var letters = ['f', '8', '0'];

function random_letter(){
    return letters[Math.floor(Math.random()*letters.length)];
}
function random_color() {
    var str = '#';
    while (str.length < 4) 
        str = str+random_letter();
    return str;
}
function set_color(){
    var background = random_color();
    var text = background;
    while (text == background) {
        text = random_color();
    }

    var body = document.getElementsByTagName('body')[0];
    body.style.backgroundColor = background;
    body.style.color = text;

    return false;
}
function timer(){
    set_color();
    window.setTimeout(timer, 100);
}