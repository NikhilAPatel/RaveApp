function endRave(){
    location.replace("/");
}

function hide_instructions(){
    $("#instructions").hide();
    sessionStorage.setItem("hidden", "true");
}

function unhide_instructions(){
    $("#instructions").show();
    sessionStorage.setItem("hidden", "false");
}

function copylink(){
    const el = document.createElement('textarea');
    el.value = "https://ravebynikhil.herokuapp.com/"+sessionStorage.getItem('room_number');
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}