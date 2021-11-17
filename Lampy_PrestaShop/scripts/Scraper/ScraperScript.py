# coding=utf8
from bs4 import BeautifulSoup
import requests
import time

from PageModel import PageModel
from ProductModel import ProductModel
from CombinationModel import CombinationModel

start_time = time.time()
def initializer():
    pages = []
    pages.append(PageModel("nowoczesne-kinkiety-scienne,29", "KINKIETY"))
    pages.append(PageModel("lampy-biurkowe-stolowe,28", "LAMPY BIURKOWE"))
    pages.append(PageModel("klasyczne-lampy-i-zyrandole,32", "ŻYRANDOLE"))
    pages.append(PageModel("lampki-dzieciece-lampy-do-pokoju-dziecka,24", "DZIECIĘCE"))
    pages.append(PageModel("lampy-lazienkowe,23", "ŁAZIENKOWE"))
    pages.append(PageModel("zarowki-led-energooszczedne,56", "ŻARÓWKI"))
    
    return pages

mainUrl = "https://www.imperiumlamp.pl/"
productsIdInUrl = "products"
productValueSubstring = "product-cell product-main-cell"
lamps = []
id = 0
pages = initializer()
file = open('productsInCSV.csv', 'w', encoding='utf-8')
file.write("ID;Aktywny (0 lub 1);Nazwa;Kategorie (x,y,z…);Cena zawiera podatek. (brutto);ID reguły podatku;Koszt własny;W sprzedaży (0 lub 1);Wartość rabatu;Procent rabatu;Rabat od dnia (rrrr-mm-dd);Rabat do dnia (rrrr-mm-dd);Indeks #;Kod dostawcy #;Dostawca;Marka;EAN13;UPC;Ecotax;Szerokość;Wysokość;Głębokość;Waga;Czas dostawy produktów dostępnych w magazynie:;Czas dostawy wyprzedanych produktów z możliwością rezerwacji:;Ilość;Minimalna ilość;Niski poziom produktów w magazynie;Wyślij do mnie e-mail, gdy ilość jest poniżej tego poziomu;Widoczność;Dodatkowe koszty przesyłki;Jednostka dla ceny za jednostkę;Cena za jednostkę;Podsumowanie;Opis;Tagi (x,y,z…);Meta-tytuł;Słowa kluczowe meta;Opis meta;Przepisany URL;Etykieta, gdy w magazynie;Etykieta kiedy dozwolone ponowne zamówienie;Dostępne do zamówienia (0 = Nie, 1 = Tak);Data dostępności produktu;Data wytworzenia produktu;Pokaż cenę (0 = Nie, 1 = Tak);Adresy URL zdjęcia (x,y,z…);Tekst alternatywny dla zdjęć (x,y,z…);Usuń istniejące zdjęcia (0 = Nie, 1 = Tak);Cecha(Nazwa:Wartość:Pozycja:Indywidualne);Dostępne tylko online (0 = Nie, 1 = Tak);Stan:;Konfigurowalny (0 = Nie, 1 = Tak);Można wgrywać pliki (0 = Nie, 1 = Tak);Pola tekstowe (0 = Nie, 1 = Tak);Akcja kiedy brak na stanie;Wirtualny produkt (0 = No, 1 = Yes);Adres URL pliku;Ilość dozwolonych pobrań;Data wygaśnięcia (rrrr-mm-dd);Liczba dni;ID / Nazwa sklepu;Zaawansowane zarządzanie magazynem;Zależny od stanu magazynowego;Magazyn;Akcesoria (x,y,z…)")
file.close()

def get_content(url, prodID):
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    products = soup.find(id = prodID)
    return products

def get_images(productInfo):
    images = productInfo.find_all("img")
    mainPhoto = images[0]
    logo = images[3]
    return mainUrl+mainPhoto["src"], mainUrl+logo["src"]

def get_header(url):
    content = get_content(url, "productHead")
    return content.find("h2").next

def get_top_table(productInfo):
    keys = productInfo.find_all("dt")
    values = productInfo.find_all("dd")
    topTable = "<dl>"
    for i in range(len(keys)):
        if keys[i].text != "Na stanie:":
            if(i == 0):
                topTable += "<dt>" + keys[i].text + "</dt>"
                topTable += "<dd>" + values[i].text + "</dd>"
                producer = values[i].text
            else:
                topTable += "<dt>" +keys[i].text + "</dt>"
                topTable += "<dd>" + values[i].text + "</dd>"
    topTable += "</dl>"
    return producer, topTable

def get_bottom_table(productInfo):
    keys = productInfo.find_all("li")
    bottomTable = "<span>Dane techniczne</span><dl>"
    for key in keys:
        li = key.text.split(':')[0]
        #if
        try:
            em = key.text.split(':')[1] 
        except:
            em = ""
        bottomTable += "<dt>"+ li + "</dt><dd>" + em + "</dd>"
    bottomTable += "</dl>"
    return bottomTable

for page in pages:

    if page.title == "LAMPY BIURKOWE":
        combinations_start_index=id+1

    if page.title == "ŻYRANDOLE":
        combinations_end_index=id+1

    url = page.url
    title = page.title
    products = get_content(mainUrl + url, productsIdInUrl)
    results = products.find_all("div", lambda value: value and value.startswith(productValueSubstring))
    for result in results:
        id += 1
        href = result.find("a").attrs['href']
        link = requests.get(mainUrl + href)
        content = link.text
        soup = BeautifulSoup(content, "html.parser")
        main = soup.find("main")
        header = main.find("h2").text
        mainPhoto, logo = get_images(main)
        amount = ""
        try:
            amount_text = main.find("dd", class_="stock").text
            amount = amount_text.split(' ')[0]
        except:
            amount = ""
        try:
            shortDesc = main.find_all("h2")[1].text
            if not isinstance(shortDesc, str):
                shortDesc = ""
        except:
            shortDesc = ""  
        producer, topTable = get_top_table(main)
        price = main.find("div", id = "price").text.split("\n")[1]
        bottomTable = get_bottom_table(main)
        lamp = ProductModel(id, header, title, price, producer, amount, topTable, bottomTable, url, mainPhoto, logo)
        product = "\n" + lamp.convert_to_CSV() 
        with open('productsInCSV.csv', 'a', encoding='utf-8') as file:
            file.write(product)
file.close()

file = open('combinationsInCSV.csv', 'w', encoding='utf-8')
file.write("Product ID*;Attribute (Name:Type:Position)*;Value (Value:Position)*;Supplier reference;Reference;EAN13;UPC;Wholesale price;Impact on price;Ecotax;Quantity;Minimal quantity;Low stock level;Impact on weight;Default (0 = No, 1 = Yes);Combination available date;Image position;Image URLs (x,y,z...);Image alt texts (x,y,z...);ID / Name of shop;Advanced Stock Managment;Depends on stock;Warehouse")
file.close()
for x in range(combinations_start_index,combinations_end_index):
    combination = CombinationModel(x,True)
    combination = "\n"+ combination.convert_to_CSV()
    with open('combinationsInCSV.csv', 'a', encoding='utf-8') as file:
            file.write(combination)
    combination = CombinationModel(x,False)
    combination = "\n"+ combination.convert_to_CSV()
    with open('combinationsInCSV.csv', 'a', encoding='utf-8') as file:
            file.write(combination)

file.close()