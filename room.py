import time
import random
import json

class Room:
    def __init__(self, room_number, cpm, colors, created, spotify_room):
        self.dead = True
        self.cpm = cpm
        self.version=0
        self.room_number = room_number
        self.colors = colors[1:].split("#")
        self.created = created
        self.spotify_room = spotify_room

    def __str__(self):
        return "Dead: "+(str)(self.dead)+", CPM: "+(str)(self.cpm)+", Colors: "+(str)(self.colors)
    

def generate_room_number():
    rooms = get_rooms()
    room_number = (str)(random.randint(100000, 999999))
    while room_number in rooms.keys():
        room_number = (str)(random.randint(100000, 999999))
    
    return room_number

def get_rooms():
    with open("rooms.txt", "r") as my_file_read:
        rooms = json.load(my_file_read)

    return rooms


def update_room(room_number, new_colors, new_cpm):
    rooms = get_rooms()
    rooms[room_number][room_number]["colors"] = new_colors
    rooms[room_number][room_number]["cpm"] = new_cpm
    rooms[room_number][room_number]["version"] = rooms[room_number][room_number]["version"]+1
    with open("rooms.txt", "w") as my_file:
        obj = json.dump(rooms, my_file)


def add_room(room_number, cpm, colors, created, dead, spotify_room):
    newRoom = {
        room_number: {
            'cpm': cpm,
            'colors': colors,
            'created': created,
            'dead': dead,
            'version': 0,
            'room_number': room_number,
            'spotify_room': spotify_room
        }
    }

    rooms = get_rooms()
    rooms[room_number] = newRoom

    with open("rooms.txt", "w") as my_file:
        obj = json.dump(rooms, my_file)

def return_room(room_number, new_song):
    room = None
    rooms = get_rooms()
    try:
        room = rooms[room_number]
    except(KeyError):
        return{
            "success": False,
            "room_number": room_number,
            "error": "value error"
        }

    except(ValueError):
        return{
            "success": False,
            "error": "value error"
        }

    return{
        "success": True,
        "newSong": new_song,
        "room_number": room_number,
        "colors": room[room_number]['colors'],
        "cpm": room[room_number]['cpm'],
        "created": room[room_number]['created'],
        "version": room[room_number]['version'],
        "spotify_room": room[room_number]['spotify_room']
    }