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
    print()
    print(rooms)
    print()
    
    def message(room_number, color):
        socketio.emit("colorChange", color, room=room_number, broadcast=True)
    
    def startRave(room):
        i = 0
        while not room.dead:
            print(room.room_number)
            message(int(room.room_number), room.colors[i%len(room.colors)])
            i+=1
            #TODO real timing
            time.sleep(1)
    
    room = rooms[int(room_number)]
    
    join_room(room_number)
    print(room_number)
    message(room_number, "9042gig819048")
    socketio.emit("colorChange", "928398129038", room=room_number)
    room.dead=False
    i=0
    while not room.dead:
        print(room.room_number)
        socketio.emit("colorChange", room.colors[i%len(room.colors)], room=room_number)
        message(int(room.room_number), room.colors[i%len(room.colors)])
        i+=1
        #TODO real timing
        time.sleep(1)

    if(room.dead):
        room.dead=False
        # x = threading.Thread(target=startRave, args=(room,))
        # x.start()
        startRave(room)

    print("joined room"+(str)(room_number))







#TODO
# # Supposed to catch 404 errors
# @app.errorhandler(404)
# def fourOfour(request):
#     return render_template('404.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    seed(872340789023)
    app.run(debug=True)
