import pickle as pkl
import requests
from requests import api
import json



'''
Class Users -> to validate the credentials or to register the user to the platform!
1) check -> to check if the username and password is correct
2) register -> to register to the platform
'''
class Users:
    def __init__(self,username=None,password=None):
        try:
            self.db = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\userDatabase.pkl","rb"))
                        
        except:
            self.db = None
        self.check(username, password)

    def check(self,username,password):
        if self.db != None:
            if username in self.db and self.db[username]==password:
                print("Successfully logged in")
                return 
            else:
                print("incorrect credentials")
                choice = input("register?\n")
                if choice.lower()=="yes" or choice.lower()=="y":
                    self.register()
                else:
                    return 
        else:
            choice = input("no username found in database. register?\n")
            if choice.lower()=="yes" or choice.lower()=="y":
                self.register()
            else:
                return 
    
    def register(self):
        clientOrShop = input("Registration as a Client or as a Shopowner (please enter 'client' or 'shop'): ")
        while clientOrShop.lower()!="client" and clientOrShop.lower()!="shop":
            print("Incorrect text entered!")
            clientOrShop = input("Registration as a Client or as a Shopowner (please enter 'client' or 'shop'): ")
        username = input("Enter your username: ")
        if self.db!=None:
            requiredDb = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\userDatabase.pkl","rb"))
            requiredDb = requiredDb[clientOrShop]
            while(username in requiredDb):
                print("Username already taken. please enter another username! ")
                username = input("Enter your username: ")
            
        password = input("Enter your password: ")
        passwordCheck = input("Enter your password again: ")
        while password!=passwordCheck:
            print("the passwords dont match. enter the password again!")
            password = input("Enter your password: ")
            passwordCheck = input("Enter your password again: ")
        try:
            db = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\userDatabase.pkl","rb"))
            if clientOrShop in db:
                db[clientOrShop][username] = password
            else:
                ToBeSaved = {}
                ToBeSaved[username]=password
                db[clientOrShop] = ToBeSaved
            pkl.dump(db,open(r"C:\college\Github_improvement\MedicalStore\userDatabase.pkl","wb"))
        except:
            db={}
            ToBeSaved = {}
            ToBeSaved[username]=password
            db[clientOrShop] = ToBeSaved
            pkl.dump(db,open(r"C:\college\Github_improvement\MedicalStore\userDatabase.pkl","wb"))
        print("successfully registered")
        print(db)


'''
Class Shop -> Contains Functions required for Shop Owner 
1) register -> registering the shop to the platform
2) FindLocation -> finding the latitude and longitude of the shop based on IP address
3) ReStock -> if the stock is less to StockUp
4) Remove -> to remove the shop from the platform
5) StockAlert -> to alert the shop owner if the stock is less than 4
'''
class Shop:
    def __init__(self):
        try:
            self.AdminData = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        except:
            self.AdminData = None
    def register(self):
        name_of_owner = input("Enter your name: ")
        name_of_shop = input("Enter the name of the shop: ")
        address_of_shop = input("Address of the shop: ")
        lat,lon = self.FindLocation()
        Stock = int(input("Enter the stocks: "))
        if self.AdminData!=None:
            if (lat,lon) not in self.AdminData:
                self.AdminData[(lat,lon)] = {"Owner": name_of_owner,"Shop":name_of_shop,"Address":address_of_shop,"Stock":Stock}        
            else:
                print("The Shop is already registered!")
            pkl.dump(self.AdminData,open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","wb"))
        else:
            self.AdminData = {}
            self.AdminData[(lat,lon)] = {"Owner": name_of_owner,"Shop":name_of_shop,"Address":address_of_shop,"Stock":Stock}  
            pkl.dump(self.AdminData,open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","wb"))

    def FindLocation(self):
        req = requests.get('https://get.geojs.io/')
        ip_req = requests.get('https://get.geojs.io/v1/ip.json')
        ipAdd = ip_req.json['ip']
        url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
        geo_req = requests.get(url)
        geo_data = geo_req.json()
        lat = geo_data['latitude']
        lon = geo_data['longitude']
        return lat,lon
  
    def ReStock(self):
        shop = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        lat,lon = self.FindLocation()
        Stock = input("Enter the stocks: ")
        shop[(lat,lon)]["Stock"] = Stock
        pkl.dump(shop,open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","wb"))
        print(shop)

    def Remove(self):
        lat,lon = self.FindLocation()
        shop = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        del shop[(lat,lon)]
        pkl.dump(shop,open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","wb"))
    
    def StockAlert(self):
        shop = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        for key,val in shop.items():
            if val["Stock"]<4:
                choice = input("Stock is less!\n ")            
                if choice.lower()=="yes" or choice.lower()=="y":
                    self.ReStock()

class Client:
    def __init__(self):
        try:
            self.client = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ClientData.pkl","rb"))
        except:
            self.client = None

    def MedicalStoreNearMe(self):
        print("inside function")
        api = 'AIzaSyAe9jJPBAmcSDeVDAueA9kPfViWb7tv4tk'
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
        r = requests.get(url+'query='+'medical stores near me'+'&key='+api)
        x = r.json() 
        y = x['results'] 
        print(y)
        for i in y:
            print(i['name'])

if __name__ == "__main__":

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    client = Client()
    client.MedicalStoreNearMe()

