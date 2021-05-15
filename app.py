from flask import (
    Flask,
    render_template,
    request
)
from flask_cors import CORS
from random import(seed, randint)
from room import Room


# Create the application instance
app = Flask(__name__, template_folder="templates")
CORS(app)

# Instantiate the list of rooms
rooms = {}

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
    
    rooms[room_number]=Room(cpm, colors)

    print(rooms[room_number])

    return {
        "room_number": room_number
    }    

#TODO
# # Supposed to catch 404 errors
# @app.errorhandler(404)
# def fourOfour(request):
#     return render_template('404.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    seed(872340789023)
    app.run(debug=True)
