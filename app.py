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
from datetime import datetime


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
    
    dt = datetime.now()
    
    rooms[room_number]=Room(room_number, cpm, colors, dt.microsecond)

    return {
        "room_number": room_number,
    }

@app.route('/rave')
def start_rave():
    room_number = request.args.get("room_number")    
    room = None

    #If this room does not exist, let the client know
    try:
        room = rooms[int(room_number)]
    except(KeyError):
        #If it can't find the key, wait a few seconds and try again before failing
        found = False
        for i in range(0, 500):
            try:
                room = rooms[int(room_number)]
                found = True
            except(KeyError):
                print(rooms)
            if(found==True):
                break
            time.sleep(.01)
        
        if(not found):
            return{
                "success": False,
                "error": "value error"
            }
        
        return{
            "success": True,
            "colors": room.colors,
            "cpm": room.cpm,
            "created": room.created
        }
    
    except(ValueError):
        return{
            "success": False,
            "error": "value error"
        }
    
    return{
        "success": True,
        "colors": room.colors,
        "cpm": room.cpm,
        "created": room.created
    }

@app.route('/joinRoom')
def join_rave():
    room_number = request.args.get("room_number")    
    
    #If this room does not exist, let the client know
    try:
        room = rooms[int(room_number)]
    except(KeyError):
        return{
            "success": False
        }
    except(ValueError):
        return{
            "success": False
        }
    
    return{
        "success": True
    }

@app.route('/<room_number>')
def rave(room_number):
    return render_template('rave.html')



#TODO
# Supposed to catch 404 errors
@app.errorhandler(404)
def fourOfour(request):
    return render_template('index.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    seed(872340789023)
    app.run(debug=False)
