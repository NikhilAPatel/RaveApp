function start_spotify_rave(){
    $.ajax({
        url:"startSpotifyRave",
        success: function(res){
            console.log(res)
            $("#roomNumber").html("&nbspRoom Number: "+res.room_number);
            updateSessionStorage(res);
            doRave();
        }
    })
}

function updateSessionStorage(res){
    sessionStorage.setItem("id", res.id)
    sessionStorage.setItem("room_number", res.room_number)
    sessionStorage.setItem("colors", JSON.stringify(res.colors));
    sessionStorage.setItem("cpm", res.cpm);
    sessionStorage.setItem("created", res.created);
    sessionStorage.setItem("spotify_room", res.spotify_room)
    sessionStorage.setItem("version", res.version)
}

async function doRave(){
    ajaxupdater();
    while(true){
        var cpm = sessionStorage.getItem("cpm");
        var colors = JSON.parse(sessionStorage.getItem("colors"));
        var created = sessionStorage.getItem("created")
        duration = (60/cpm)*1000
        currentdate = new Date();
        time_passed = currentdate-created;
        //Determine what color it should be right now
        index = time_passed%(duration*colors.length)
        index = parseInt(index/duration)
        document.body.style.background="#"+colors[index];

        await new Promise(r => setTimeout(r, 1));
    }
}

async function rave(room_number){
    $.ajax({
        url:"rave",
        data:{
            "room_number":  room_number
        },
        success: function(res){
            console.log(res)
            if(!res.success){
                location.replace("/");
                return;
            }
            updateSessionStorage(res);
            doRave();
        }
    })
}