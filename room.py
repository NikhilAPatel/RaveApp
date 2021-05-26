import time

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
    

