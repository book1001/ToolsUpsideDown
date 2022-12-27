// Meun Buttons ------------------------------------------------

// function menuSyllabus() {
//   document.getElementById("menuSyllabus").style.display = "block";
//   document.getElementById("menuSchedule").style.display = "none";
//   document.getElementById("menuArena").style.display = "none";
// }
//
// function menuSchedule() {
//   document.getElementById("menuSyllabus").style.display = "none";
//   document.getElementById("menuSchedule").style.display = "block";
//   document.getElementById("menuArena").style.display = "none";
// }

// function menuArena() {
//   // document.getElementById("menuSyllabus").style.display = "none";
//   // document.getElementById("menuSchedule").style.display = "none";
//   document.getElementById("areaIframe").style.display = "block";
// }

function menuArena() {
    if (document.getElementById("areaIframe").style.display === "none") {
  
      document.getElementById("areaIframe").style.display = "block";
      document.getElementById("menuArenaId").style.transform = "scaleY(-1)";
    }
    else {
      document.getElementById("areaIframe").style.display = "none";
      document.getElementById("menuArenaId").style.transform = "none";
    }
  }
  
  // function menuArena(button)
  // {
  //   if(document.getElementById("menuArena").value=="OFF") {
  //    document.getElementById("menuArena").value="ON";
  //    document.getElementById("areaIframe").style.display = "block";
  //  }
  //
  //   else if(document.getElementById("menuArena").value=="ON") {
  //    document.getElementById("menuArena").value="OFF";
  //    document.getElementById("areaIframe").style.display = "none";
  //  }
  // }
  
  
  
  // iFrame: Draggable ------------------------------------------------
  
  // $(".draggable").draggable({
  //   handle: ".handle",
  //   iframeFix: true,
  //   start: function(event, ui) {
  //     $('.frameOverlay').show();
  //   },
  //   stop: function(event, ui) {
  //     $(".frameOverlay").hide();
  //   }
  // });
  
  
  // Random Moving Div ------------------------------------------------
  
  $(document).ready(function(){
      animateDiv('.a');
      animateDiv('.b');
      animateDiv('.c');
      animateDiv('.d');
  });
  
  function makeNewPosition(){
  
      // Get viewport dimensions (remove the dimension of the div)
      var h = $(window).height() - 50;
      var w = $(window).width() - 50;
  
      var nh = Math.floor(Math.random() * h);
      var nw = Math.floor(Math.random() * w);
  
      return [nh,nw];
  
  }
  
  function animateDiv(myclass){
      var newq = makeNewPosition();
      var oldq = $(myclass).offset();
      var speed = calcSpeed([oldq.top, oldq.left], newq);
      $(myclass).animate({ top: newq[0], left: newq[1] }, speed,   function(){
        animateDiv(myclass);
      });
  
  };
  
  function calcSpeed(prev, next) {
  
      var x = Math.abs(prev[1] - next[1]);
      var y = Math.abs(prev[0] - next[0]);
  
      var greatest = x > y ? x : y;
  
      var speedModifier = 0.05;
  
      var speed = Math.ceil(greatest/speedModifier);
  
      return speed;
  
  }