from bs4 import BeautifulSoup
import urllib.request as ur

class Bok3:
    
    service_list = []

    def __init__(self):
        pass

    def add_service(self, service):
        if service not in self.service_list:
            self.service_list.append(service)

    def search_isbn(self, isbn):
        isbn = int(isbn)
        result = []

        for service in self.service_list:
            tmp_object = service.search(isbn)
            for book in tmp_object:
                result.append(book)

        return result

class Adlibris:
    
    def __init__(self, observer):
        observer.add_service(self)

    def search(self, isbn):
        result = []

        url = "https://www.adlibris.com/se/sok?q=" + str(isbn)
        ugly = ur.urlopen(url)

        soup = BeautifulSoup(ugly)
        found_items = soup.find_all(class_="product-item")

        for item in found_items:
            title_obj = item.find("img")
            title = title_obj.get("alt")
            price_obj = item.find(class_="current-price")
            price = int(price_obj.contents[0])
            link_obj = item.find("a", class_="notify")
            link = "https://www.adlibris.com" + link_obj.get("href")

            book_obj = {"title": title, "price": price, "href": link, 
                "store": "Adlibris"}
            result.append(book_obj)

        return result 

class Bokus:
    def __init__(self, observer):
        observer.add_service(self)

    def search(self, isbn):
        result = [] 
        url = "http://www.bokus.se/bok/" + str(isbn)
        ugly = ur.urlopen(url)

        soup = BeautifulSoup(ugly)
        title_obj = soup.find("h1").find("span")
        title = title_obj.contents[0]
        price_obj = soup.find(id="price-row").find(class_="pris")
        price = int(price_obj.get("content"))

        result.append({"title": title, "price": price, "href": url, 
            "store": "Bokus"})

        return result

main = Bok3()
Adlibris(main)
Bokus(main)
print(main.search_isbn(9789144031194))
