// Demo buttons: explain what they'll do on the live site instead of ringing a number that isn't set up yet.
(function(){
  var toast = document.getElementById("toast"), t = 0;
  function show(msg){
    toast.textContent = msg; toast.classList.add("on");
    clearTimeout(t); t = setTimeout(function(){ toast.classList.remove("on"); }, 2600);
  }
  Array.prototype.forEach.call(document.querySelectorAll(".demo"), function(a){
    a.addEventListener("click", function(e){ e.preventDefault(); show(a.getAttribute("data-msg")); });
  });
})();
