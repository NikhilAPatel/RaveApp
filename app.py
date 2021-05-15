from flask import (
    Flask,
    render_template,
    request
)
from flask_cors import CORS
from flask_socketio import (SocketIO, join_room, leave_room)
from random import(seed, randint)
from room import Room
import threading
import time


# Create the application instance
app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app)
CORS(app)

# Instantiate the list of rooms
rooms = {}
threads = {}

# Create a URL route in our application for "/"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createRoom')
def create_room():
    cpm = request.args.get("cpm")
    colors = request.args.get("colors")
    
    # Generate room number
    room_number = randint(0, 1000000)
    while room_number in rooms.keys():
        room_number = randint(0, 1000000)
    
    rooms[room_number]=Room(room_number, cpm, colors)

    return {
        "room_number": room_number
    }

@app.route('/<room_number>')
def rave(room_number):
    return render_template('rave.html')


@socketio.on('join')
def on_join(data):
    room_number = data['room_number']    
    room = rooms[int(room_number)]
    
    join_room(room_number)
    
    if(room.dead):
        room.dead=False
        i=0
        room.time_since_verify=0
        room.awaiting_verfiy=False
        while not room.dead:
            print(room.dead)
            print("emitting to room " + room_number)
            socketio.emit("colorChange", room.colors[i%len(room.colors)], room=room_number)
            i+=1
            
            #Checking periodically to make sure people are still raving
            if(i%10==0):
                print("emitting verification")
                socketio.emit("checkAlive", "Anyone there?", room=room_number)
                room.awaiting_verify=True
            
            if(room.awaiting_verify):
                print(room.time_since_verify)
                room.time_since_verify +=1
            
            #Close the room if no client has verified in 100 cycles
            if(room.time_since_verify>100):
                room.dead=True
            
            #TODO real timing
            time.sleep(.1)

@socketio.on('confirmAlive')
def on_aliveConfirmation(data):
    rooms[int(data['room_number'])].awaiting_verify=False
    rooms[int(data['room_number'])].time_since_verify=0





@socketio.on('end')
def on_end(data):
    rooms[int(data['room_number'])].dead=True


#TODO
# # Supposed to catch 404 errors
# @app.errorhandler(404)
# def fourOfour(request):
#     return render_template('404.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    seed(872340789023)
    app.run(debug=True)
