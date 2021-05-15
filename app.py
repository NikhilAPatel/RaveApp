from flask import (
    Flask,
    render_template,
    request
)
from flask_cors import CORS


# Create the application instance
app = Flask(__name__, template_folder="templates")
CORS(app)

# Instantiate the list of rooms
rooms = []

# Create a URL route in our application for "/"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createRoom')
def create_room():
    room_number = request.args.get("room_number")
    if room_number not in rooms:
        rooms.append(room_number)
    return {
        "rooms": tuple(rooms)
    }    

#TODO
# # Supposed to catch 404 errors
# @app.errorhandler(404)
# def fourOfour(request):
#     return render_template('404.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
