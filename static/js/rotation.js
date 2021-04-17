window.onload = function(){
  var showInfo = document.querySelector(".showInfo");
  var table = showInfo.querySelector("table");
  startMove(table,{"top":"600"})
}

function getStyle(obj,name){
  if(obj.currentStyle){
      return obj.currentStyle[name];
  }
  else{
      return getComputedStyle(obj,null)[name];
  }
}
function startMove(obj,json,EndFun){
  clearInterval(obj.time);
  obj.time=setInterval(function(){
      for(var i in json){
      var cur=0;
      var bStop=true;
      if(i=="opacity"){
          cur=Math.round(parseFloat(getStyle(obj,i))*100);
      }
      else{
          cur=parseInt(getStyle(obj,i));
      }
      speed= -1
      if(cur!=json[i]){
          bStop=false;
      }
          if(i=="opacity"){
              obj.style.filter="alpha(opacity="+cur+speed+")";
              obj.style.opacity=(cur+speed)/100;
          }
          else{
              obj.style[i]=cur+speed+"px";
          }
  }
  if(bStop){
      clearInterval(obj.time);
      if(EndFun){
          EndFun();
      }
  }
  },30)
}