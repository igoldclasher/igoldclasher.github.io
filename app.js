let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = "#FFFFFF";
tg.MainButton.color = "#2cab37";

let item= "";

let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5");
let btn6 = document.getElementById("btn6");
let btn7 = document.getElementById("btn7");
let btn8 = document.getElementById("btn8");
let btn9 = document.getElementById("btn9");
let btn10 = document.getElementById("btn10");
let btn11 = document.getElementById("btn11");
let btn12 = document.getElementById("btn12");
let btn13 = document.getElementById("btn13");
let btn14 = document.getElementById("btn14");
let btn15 = document.getElementById("btn15");
let btn16 = document.getElementById("btn16");
let btn17 = document.getElementById("btn17");
let btn18 = document.getElementById("btn18");
let btn19 = document.getElementById("btn19");
let btn20 = document.getElementById("btn20");
let btn21 = document.getElementById("btn21");
let btn22 = document.getElementById("btn22");
let btn23 = document.getElementById("btn23");
let btn24 = document.getElementById("btn24");
let btn25 = document.getElementById("btn25");
let btn26 = document.getElementById("btn26");
let btn27 = document.getElementById("btn27");
let btn28 = document.getElementById("btn28");


btn1.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
        tg.MainButton.setText("Добавить в корзину1!");
        item = "1";
        tg.MainButton.show();
    }
    else {
        tg.MainButton.setText("Добавить в корзину1!");
        item = "1";
        tg.MainButton.show();
    }
});

btn2.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
        tg.MainButton.setText("Добавить в корзину2!");
        item = "2";
        tg.MainButton.show();
    }
    else {
        tg.MainButton.setText("Добавить в корзину2!");
        item = "2";
        tg.MainButton.show();
    }
});

btn3.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
        tg.MainButton.setText("Добавить в корзину3!");
        item = "3";
        tg.MainButton.show();
    }
    else {
        tg.MainButton.setText("Добавить в корзину3!");
        item = "3";
        tg.MainButton.show();
    }
});

btn4.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
        tg.MainButton.setText("Добавить в корзину4!");
        item = "4";
        tg.MainButton.show();
    }
    else {
        tg.MainButton.setText("Добавить в корзину4!");
        item = "4";
        tg.MainButton.show();
    }
});

btn5.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
        tg.MainButton.setText("Добавить в корзину5!");
        item = "5";
        tg.MainButton.show();
    }
    else {
        tg.MainButton.setText("Добавить в корзину5!");
        item = "5";
        tg.MainButton.show();
    }
});

btn6.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
        tg.MainButton.setText("Добавить в корзину6!");
        item = "6";
        tg.MainButton.show();
    }
    else {
        tg.MainButton.setText("Добавить в корзину6!");
        item = "6";
        tg.MainButton.show();
    }
});


Telegram.WebApp.onEvent("mainButtonClicked", function(){
    tg.sendData(item);
});

let usercard = document.getElementById("usercard");

let p = document.createElement("p");

p.innerText = `${tg.initDataUnsafe.user.first_name}
${tg.initDataUnsafe.user.last_name}`;

usercard.appendChild(p);
