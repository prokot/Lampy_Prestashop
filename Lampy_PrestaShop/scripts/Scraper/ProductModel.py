from os import waitpid


class ProductModel:
    def __init__(self, id, header, title, price, producer, amount, topTable, bottomTable, url, mainPhoto, logo):
        self.id = id
        self.header = header
        self.title = title
        self.price = price
        self.producer = producer
        self.amount = amount
        self.topTable = topTable
        self.bottomTable = bottomTable
        self.url = url
        self.mainPhoto = mainPhoto
        self.logo = logo

    def convert_to_CSV(self):
        inf = str(self.id) + ";1;" + self.header + ";" + self.title + ";" + self.price + ";1;;0;;;;;;;;"
        inf += self.producer + ";;;;;;;;;;" + self.amount + ";1;1;1;both;;;;" + self.topTable + ";"
        inf += self.bottomTable + ";" + self.producer + ";Meta title-" + str(self.id) + ";Meta keywords-" + str(self.id) + ";Meta description-" + str(self.id) + ";"
        inf += self.url + ";Dostępny;Niedostępny;1;;;1;" + self.mainPhoto + ", " + self.logo + ";;0;;0;new;0;0;0;0;0;;;;;0;0;0;0;"

        return inf

