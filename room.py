class Room:
    def __init__(self, cpm, colors):
        self.dead = False
        self.cpm = cpm
        self.colors = colors[1:].split("#")

    def __str__(self):
        return "Dead: "+(str)(self.dead)+", CPM: "+(str)(self.cpm)+", Colors: "+(str)(self.colors)