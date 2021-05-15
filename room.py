import time

class Room:
    def __init__(self, room_number, cpm, colors):
        self.dead = True
        self.cpm = cpm
        self.room_number = room_number
        self.colors = colors[1:].split("#")

    def __str__(self):
        return "Dead: "+(str)(self.dead)+", CPM: "+(str)(self.cpm)+", Colors: "+(str)(self.colors)
    

