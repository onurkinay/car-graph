var objImage = null;
var hiz = 0;
var surdur = true;
setInterval(sendHiz, 1000); 

function init() {
    objImage = document.getElementById("image1");
    objImage.style.position = 'relative';
    objImage.style.left = (parseInt(window.innerWidth)/2)+'px';
}

function getKeyAndMove(e) {
    var key_code = e.which || e.keyCode;
    if(surdur) {
        switch (key_code) {
            case 65: //left arrow key
                moveLeft();
                break;
            case 87: //Up arrow key
                moveRightAcc();
                break;
            case 68: //right arrow key
                moveRight();
                break;
            case 83: //down arrow key
                moveLeftAcc();
                break;

        }
    }
     switch (key_code) {
          case 90://Z button
              if(surdur) {
                  surdur = false;
                  $.get("/durdur", function (data, status) {
                  });
              }
              else{
                   surdur = true;

                  }
                break;
            case 88://X button
                surdur = true;
                $.get("/sifirla", function (data, status) {
                });
                break;
     }


}

function moveLeft() {
       if(parseInt(objImage.style.left, 10) > 0) {
            hiz = -10;
        objImage.style.left = parseInt(objImage.style.left) + hiz + 'px';
          if(parseInt(objImage.style.left, 10) <= 0) {
                  objImage.style.left = window.innerWidth-150 + 'px';
           }

    }
    console.log(objImage.style.left);
}

function moveLeftAcc() {

    if(parseInt(objImage.style.left, 10) > 0) {
          hiz -= 0.5;
        objImage.style.left = parseInt(objImage.style.left) + (hiz) + 'px';
          if(parseInt(objImage.style.left, 10) <= 0) {
                  objImage.style.left = window.innerWidth-150 + 'px';
           }

    }
}

function moveRight() {
      if(parseInt(objImage.style.left, 10) < window.innerWidth-150) {
            hiz = 10;
         objImage.style.left = parseInt(objImage.style.left) + hiz + 'px';
   if(parseInt(objImage.style.left, 10) > window.innerWidth-200) {
                  objImage.style.left = 0+ 'px';
           }
     }
      console.log(objImage.style.left);
}

function moveRightAcc() {
     if(parseInt(objImage.style.left, 10) < window.innerWidth-150) {
          hiz += 0.5;
         objImage.style.left = parseInt(objImage.style.left) + hiz + 'px';
           if(parseInt(objImage.style.left, 10) > window.innerWidth-200) {
                  objImage.style.left = 0+ 'px';
           }

     }
}

function sendHiz() {
    if(surdur) {
        $.get("/get-hiz?hiz=" + hiz, function (data, status) {
        });
    }
}

function Sifirla() {
    hiz = 0;
}

window.onload = init;
	