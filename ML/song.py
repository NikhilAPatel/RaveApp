class Song():
    def __init__(self, name, artist, score, id=""):
        self.name=name
        self.artist=artist
        (self.positive, self.neutral, self.negative) = score.split("_")
        self.id=id
    
    def __str__(self):
        return self.name+" - "+self.artist+" id: "+self.id+" score ("+self.positive+", "+self.neutral+", "+self.negative+")"
    
    def assign_features(self, features):
        self.danceability = (str)(features[0]['danceability'])
        self.energy = (str)(features[0]['energy'])
        self.key = (str)(features[0]['key'])
        self.loudness = (str)(features[0]['loudness'])
        self.mode = (str)(features[0]['mode'])
        self.speechiness = (str)(features[0]['speechiness'])
        self.acousticness = (str)(features[0]['acousticness'])
        self.instrumentalness = (str)(features[0]['instrumentalness'])
        self.liveness = (str)(features[0]['liveness'])
        self.valence = (str)(features[0]['valence'])
        self.tempo = (str)(features[0]['tempo'])
    
    
    def to_row(self):
        return self.name+", "+self.artist+", "+self.positive+", "+self.neutral+", "+self.negative+", "+self.danceability+", "+self.energy+", "+self.key+", "+self.loudness+", "+self.mode+", "+self.speechiness+", "+self.acousticness+", "+self.instrumentalness+", "+self.liveness+", "+self.valence+", "+self.tempo