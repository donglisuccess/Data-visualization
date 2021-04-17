// 设置时间
var t = null;
t = setTimeout(time, 1000); //開始运行
function rule(ele){
  if (ele<10){
    return "0"+ele
  }
  else{
    return ele
  }
};
function time() {
  clearTimeout(t); //清除定时器
  dt = new Date();
  var y = dt.getFullYear();
  var mt = dt.getMonth() + 1;
  var day = dt.getDate();
  var h = dt.getHours(); //获取时
  var m = dt.getMinutes(); //获取分
  var s = dt.getSeconds(); //获取秒
  document.querySelector("showTime").innerHTML = 
  rule(y)+"-"+rule(mt)+"-"+rule(day)+"  "+rule(h)+":"+rule(m)+":"+rule(s)
  t = setTimeout(time, 1000); //设定定时器，循环运行
}
time()