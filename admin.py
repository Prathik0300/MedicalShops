import pickle as pkl
import requests
from requests import api
import requests
import json
from googlemaps import convert

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
        
        try:
            self.client = self.db['client']         
        except:
            self.client =None

        try:
            self.shop = self.db['shop']         
        except:
            self.shop =None
        self.check(username, password)


    def check(self,username,password):
        if self.client==None and self.shop==None:
            choice = input("no username found in database. register?\n")
            if choice.lower()=="yes" or choice.lower()=="y":
                self.register()
                return 
            else:
                return 
                
        if self.db != None:
            if self.client!=None:
                if username in self.client and self.client[username]==password:
                    print("Successfully logged in")
                    return ClientSideFunctions()
            if self.shop!=None:
                if username in self.shop and self.shop[username]==password:
                    print("Successfully logged in")
                    return ShopFunctions()
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
        while clientOrShop!="client" and clientOrShop!="shop":
            print("Incorrect text entered!")
            clientOrShop = input("Registration as a Client or as a Shopowner (please enter 'client' or 'shop'): ")
        username = input("Enter your username: ")
        if self.db!=None:
            Db = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\userDatabase.pkl","rb"))
            requiredDb = Db[clientOrShop]
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
    def Register(self):
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
        print(pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb")))

    def FindLocation(self):
        req = requests.get('https://get.geojs.io/')
        ip_req = requests.get('https://get.geojs.io/v1/ip.json')
        ipAdd = ip_req.json()['ip']
        url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
        geo_req = requests.get(url)
        geo_data = geo_req.json()
        lat = geo_data['latitude']
        lon = geo_data['longitude']
        return lat,lon
  
    def ReStock(self):
        try:
            shop = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        except:
            shop = None
        if shop!=None:
            print("inside the restock function")
            lat,lon = self.FindLocation()
            if (lat,lon) in shop:
                print("inside the restock function1")
                Stock = int(input("Enter the stocks: "))
                print("inside the restock function2")
                shop[(lat,lon)]["Stock"] = Stock
                print("inside the restock function3")
                pkl.dump(shop,open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","wb"))
                print("inside the restock function4")
                print(shop)
                print("inside the restock function5")
            else:
                print("No shop!")
        else:
            print("There are no shops available in the database!")

    def Remove(self):
        try:
            shop = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        except:
            shop = None

        if shop!=None:
            lat,lon = self.FindLocation()
            if (lat,lon) in shop:
                del shop[(lat,lon)]
                pkl.dump(shop,open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","wb"))
            else:
                print("No shop is registered!")
        else:
            print("There are no shops available in the database!")

    def StockAlert(self):
        try:
            shop = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        except:
            shop =None
        if shop!=None:
            for key,val in shop.items():
                if val["Stock"]<4:
                    choice = input("Stock is less in "+val['Shop'])            
                    if choice.lower()=="yes" or choice.lower()=="y":
                        self.ReStock()
                    
'''
Class Client -> Contains Functions required for Clients
1) MedicalStoreNearMe() -> To find the list of Medical shops near the user who have stocks. if the shop does not have stock then it wont be listed to the user
2) FindDirections() -> To find the directions to the required/selected medical shop from the list of shops shown
'''
class Client:
    def __init__(self):
        try:
            self.client = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ClientData.pkl","rb"))
        except:
            self.client = None

    def MedicalStoreNearMe(self):
        api = 'AIzaSyAe9jJPBAmcSDeVDAueA9kPfViWb7tv4tk'
        try:
            shop = pkl.load(open(r"C:\college\Github_improvement\MedicalStore\ShopData.pkl","rb"))
        except:
            shop = None
        if shop!=None:
            url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
            r = requests.get(url+'query='+'medical stores near me'+'&key='+api)
            x = r.json() 
            y = x['results'] 
            self.NearByMedicalShops = {}
            index=0
            for idx,i in enumerate(y):
                lat = i['latitude']
                lon = i['longitude']
                if ((i[lat],i[lon]) in shop) and (shop[(i[lat],i[lon])]["Stock"]!=0):
                    print(index," ",i["name"])
                    self.NearByMedicalShops[index] = (i['name'],idx)
                    index+=1
            if not self.NearByMedicalShops:
                print("Sorry there are no medical shops near :(")
                return 
            DirectionToTheRequiredLoc = int(input("Enter the index of the shop you want to go: "))
            while DirectionToTheRequiredLoc not in self.NearByMedicalShops:
                print("The Entered index is not in the List! Please enter again...")
                DirectionToTheRequiredLoc = int(input("Enter the index of the shop you want to go: "))
            self.FindDirections(DirectionToTheRequiredLoc,y)
        else:
            print("There are no shops available in the database!")

    def FindDirections(self,index,data):
        LocInfo = data[self.NearByMedicalShops[index][1]]
        LocLat = LocInfo['latitude']
        LocLon = LocInfo['longitude']
        myLat,myLon = Shop().FindLocation()
        api_key = 'AIzaSyAe9jJPBAmcSDeVDAueA9kPfViWb7tv4tk'
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='
        r = requests.get(url+myLat,myLon+'&destination='+LocLat,LocLon+'&key='+api_key)
        x=r.json()
        y=x['results']
        print(y)
'''
class Shutdown -> this class is for ending/closing the platform functions i.e while exiting the  platform
'''
class Shutdown:
    def __init__(self):
        print('Have a Nice Day!')
        return 

if __name__ == "__main__":

    '''
    ClientSideFunctions() -> function responsible to take input from the user and performs the required action till he/she decides to quit the platform.
    '''
    def ClientSideFunctions():
        FunctionList = ['MedicalStoreNearMe']
        client = Client()
        print("*************************************************")
        print("\n")
        print("index", " ", "Functions")
        count=0
        for idx,i in enumerate(FunctionList):
            print(idx, " ", i)
            count+=1
        command = int(input("Enter the index of the function you want to execute: "))
        while(command!=-1):
            if 0<=command<count:
                client.MedicalStoreNearMe()
            else:
                print("The index is out of bound! please enter a valid index!")
            command = int(input("Enter the index of the function you want to execute: "))
        Shutdown()

    '''
    ShopFunctions() -> this function is responsible for taking input from the shopOwners and perform the required actions till the shopOwner decides to exit the platform.
    '''
    def ShopFunctions():
        FunctionList = ['Register','ReStock','Remove']
        shop = Shop()
        print("*************************************************")
        print("\n")
        print("index", " ", "Functions")
        count=0
        for idx,i in enumerate(FunctionList):
            print(idx, " ", i)
            count+=1
        command = int(input("Enter the index of the function you want to execute: "))
        while(command!=-1):
            shop.StockAlert()
            if 0<=command<=count:
                if command==0:
                    shop.Register()
                elif command==1:
                    shop.ReStock()
                elif command==2:
                    shop.Remove()
            else:
                print("The index is out of bound! please enter a valid index!")
            command = int(input("Enter the index of the function you want to execute: "))
        Shutdown()


    username = input("Enter your username: ")
    password = input("Enter your password: ")
    Users(username,password)
    
