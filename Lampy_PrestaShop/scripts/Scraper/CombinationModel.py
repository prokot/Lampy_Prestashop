from os import waitpid
#1;Rodzaj wtyczki:select:1;Amerykańska:1;;;;;0;20;0;5;1;0;0;1dlaEuro0dlaAm;;;;;0;0;0;

class CombinationModel:
    def __init__(self, id, isEuro):
        self.id = id
        self.attribute = 'Rodzaj wtyczki:select:1'
        self.value = ("Amerykańska:1", "Europejska:1")[isEuro]
        self.additionalPrice = (0, 20)[isEuro]
        self.default = (0, 1)[isEuro]


    def convert_to_CSV(self):
        inf = str(self.id) + ";"+self.attribute+";" + self.value + ";;;;;0;"+str(self.additionalPrice)
        inf+= ";0;5;1;0;0;"+str(self.default)+";;;;;0;0;0;"
        return inf

