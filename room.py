import time

class Room:
    def __init__(self, cpm, colors):
        self.dead = False
        self.cpm = cpm
        self.colors = colors[1:].split("#")

    def __str__(self):
        return "Dead: "+(str)(self.dead)+", CPM: "+(str)(self.cpm)+", Colors: "+(str)(self.colors)
    
    def startRave(self):
        i = 0
        while not self.dead:
            print(self.colors[i%len(self.colors)])
            i+=1
            time.sleep(1)