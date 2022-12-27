import collections, datetime, itertools, re, urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson

from yourworld.helpers import req_render_to_response
from yourworld.lib import log
from yourworld.ywot.models import Tile, World, Edit, Whitelist
from yourworld.ywot import permissions

#
# Helpers
#

class ClaimException(Exception):
    pass

def fetch_updates(request, world):
    response = {}
    min_tileY = int(request.GET['min_tileY'])
    min_tileX = int(request.GET['min_tileX'])
    max_tileY = int(request.GET['max_tileY'])
    max_tileX = int(request.GET['max_tileX'])
    response = {}

    assert min_tileY < max_tileY
    assert min_tileX < max_tileX
    assert ((max_tileY - min_tileY)*(max_tileX - min_tileX)) < 400
    
    # Set default info to null
    for tileY in xrange(min_tileY, max_tileY + 1): #+1 b/c of range bounds
        for tileX in xrange(min_tileX, max_tileX + 1):
            response["%d,%d" % (tileY, tileX)] = None
            
    tiles = Tile.objects.filter(world=world,
                                tileY__gte=min_tileY, tileY__lte=max_tileY,
                                tileX__gte=min_tileX, tileX__lte=max_tileX)
    for t in tiles:
        tile_key = "%s,%s" % (t.tileY, t.tileX)
        if (int(request.GET.get('v', 0)) == 2):
            d = {'content': t.content.replace('\n', ' ')}
            if 'protected' in t.properties: # We want to send *any* set value (case: reset to false)
                d['protected'] = t.properties['protected']
            response[tile_key] = d
        elif (int(request.GET.get('v', 0)) == 3):
            d = {'content': t.content.replace('\n', ' ')}
            if t.properties:
                d['properties'] = t.properties
            response[tile_key] = d
        else:
            raise ValueError, 'Unknown JS version'
    return HttpResponse(simplejson.dumps(response))
    
def send_edits(request, world):
    assert permissions.can_write(request.user, world) # Checked by router
    response = []
    tiles = {} # a simple cache
    edits = [e.split(',', 5) for e in request.POST.getlist('edits')]
    for edit in edits:
        char = edit[5]
        tileY, tileX, charY, charX, timestamp = map(int, edit[:5])
        assert len(char) == 1 # TODO: investigate these tracebacks
        keyname = "%d,%d" % (tileY, tileX)
        if keyname in tiles:
            tile = tiles[keyname]
        else:
            # TODO: select for update
            tile, _ = Tile.objects.get_or_create(world=world, tileY=tileY, tileX=tileX)
            tiles[keyname] = tile
        if tile.properties.get('protected'):
            if not permissions.can_admin(request.user, world):
                continue    
        tile.set_char(charY, charX, char)
        # TODO: anything, please.
        if tile.properties:
            if 'cell_props' in tile.properties:
                if str(charY) in tile.properties['cell_props']: #must be str because that's how JSON interprets int keys
                    if str(charX) in tile.properties['cell_props'][str(charY)]:
                        del tile.properties['cell_props'][str(charY)][str(charX)]
                        if not tile.properties['cell_props'][str(charY)]:
                            del tile.properties['cell_props'][str(charY)]
                            if not tile.properties['cell_props']:
                                del tile.properties['cell_props']
        response.append([tileY, tileX, charY, charX, timestamp, char])
    if len(edits) < 200:
        for tile in tiles.values():
            tile.save()
        Edit.objects.create(world=world, 
                            user=request.user if request.user.is_authenticated() else None,
                            content=repr(edits),
                            ip=request.META['REMOTE_ADDR'],
                            )
    return HttpResponse(simplejson.dumps(response))

#
# Account Views
#
def home(request):
    """The main front-page other than a world."""
    world, _ = World.get_or_create("")

    if 'fetch' in request.GET:
        return fetch_updates(request, world)
    can_write = permissions.can_write(request.user, world)
    if request.method == 'POST':
        if not can_write:
            return response_403()
        return send_edits(request, world)
    state = {
        'canWrite': can_write,
        'canAdmin': permissions.can_admin(request.user, world),
        'worldName': world.name,
        'features': permissions.get_available_features(request.user, world),
    }
    if 'MSIE' in request.META.get('HTTP_USER_AGENT', ''):
        state['announce'] = "Sorry, your World of Text doesn't work well with Internet Explorer."
    return req_render_to_response(request, 'home.html', {
        'settings': settings,
        'state': simplejson.dumps(state),
    })
