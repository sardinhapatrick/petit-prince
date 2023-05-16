function setCookie(isCorrect) {
  var currentScore = getCookie("score")
  var currentHint = getCookie("hint")
  console.log(isCorrect)
  if (isCorrect == "0") {
    var newScore = parseFloat(currentScore) + parseFloat(isCorrect);
  }
  else {
    var newScore = parseFloat(currentScore) + parseFloat(isCorrect) - parseFloat(currentHint);
  }
  var newTotal = parseInt(getCookie("total")) + 1
  document.cookie = "score =" + newScore + ";";
  document.cookie = "total =" + newTotal + ";";
  document.cookie = "hint =" + "0" + ";";
  return newScore;
}

function setHint() {
  document.cookie = "hint =" + "0.5" + ";";
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function resetCookie(){
    document.cookie = "score =" + "0" + ";";
    document.cookie = "total =" + "0" + ";";
    document.cookie = "hint =" + "0" + ";";
}
