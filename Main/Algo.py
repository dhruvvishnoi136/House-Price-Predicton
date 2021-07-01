import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import pickle
import os
class Algos:
    def __init__(self, area_type=0,availability=0,location=0,size=0,society=0,sqft=0,bath=0,pps=0,  allow_test = "1"):
        self.area_type = area_type
        self.availability = availability
        self.location = location
        self.size = size
        self.society = society
        self.sqft = sqft
        self.bath = bath
        self.pps = pps
        self.allow_test = allow_test



    def data_cleaning(self):
        data = pd.read_csv("./Main/Result.csv")
        #areatype
        data["areatype"] = np.where(data["areatype"]== " Super built-up Area" , 0 
        , np.where(data["areatype"] ==" Plot Area", 1 
        , np.where(data["areatype"] ==" Carpet Area" , 2 
        , np.where(data["areatype"] == " Built-up Area" ,3 ,0))))
        #availability
        data["availability"] = np.where(data["availability"] == "READY TO MOVE" , 0 
        , np.where(data["availability"] == "UNDER CONSTRUCTION" , 1 
        ,np.where(data["availability"] == "UNKNOWN" , 3,0)))
        #location
        zipcodes = pd.read_csv("./Main/zipcodes.csv")
        for i in zipcodes.index:
            data['location'].replace(zipcodes['location'][i],int(zipcodes['zipcode'][i]),inplace=True)
        
        data['location'].replace(regex='[a-zA-z]', value=0 , inplace=True)
        #size
        data["size"].fillna("0" ,inplace=True)
        data["size"]  = (data["size"].str.replace("BHK",""))
        # Society
        data["society"] = (data['society'].notnull()).astype('int')
        data["sqft"] = data["sqft"].str.replace("sq.ft." , "")
        temp_sqft = []
        for sqft in data["sqft"]:
            if "-" in sqft :
                split_sqft = sqft.split("-")
                temp_sqft.append((int(split_sqft[0])+int(split_sqft[1]))/2)
            else:
                temp_sqft.append(int(sqft))
        data["sqft"] = temp_sqft
        # Bath
        data["bath"].fillna("0",inplace=True)
        # Price
        temp_price = []
        data["price"].fillna(str(0), inplace=True)
        for price in data["price"]:
            if "Lac" in price and "Cr" in price:
                price = price.replace("Lac" , "").replace("Cr" , "")
                price = price.split("-")
                temp_price.append((float(price[0])+(float(price[1])*100))/2)

            elif "Lac" in price:
                price = price.replace("Lac","")
                if "-" in price:
                    price = price.split("-")
                    temp_price.append(((float(price[0])+float(price[1]))/2))
                else:
                    temp_price.append(float(price))

            elif "Cr" in price:
                price = price.replace("Cr","")
                if "-" in price:
                    price = price.split("-")
                    temp_price.append(((float(price[0])+float(price[1]))/2)*100)
                    
                else:
                    temp_price.append(float(price)*100)
            else:
                temp_price.append(float(price)/100000)
        data["price"] = temp_price
        price = lambda a : a * 100000
        data['price'] = price(data['price'])
        data = data[["price","areatype","availability" ,"location","size","society","sqft","bath"]]
        data['pps'] = (data['price'])/data['sqft']
        return data

    def knn_model(self):
        data = self.data_cleaning()
        x = data.iloc[: ,1:-1].values
        y = data.iloc[:,-1].values
        X_train, X_test, Y_train, Y_test = train_test_split(x, y , test_size=0.1, random_state=4)
        knn = KNeighborsRegressor(n_neighbors=1)
        Price_pridict_trainer = knn.fit(X_train , Y_train)
        pickle.dump(Price_pridict_trainer , open("./Main/Knn_model.pkl", 'wb'))
        if self.allow_test == "1":
            return (Price_pridict_trainer.score(X_test , Y_test))*100
        else:
            pass
        
        
    def random_model(self):
        data = self.data_cleaning()
        x = data.iloc[:,1:].values
        y = data.iloc[:,:1].values
        X_train, X_test, Y_train, Y_test = train_test_split(x, y , test_size=0.2 , random_state=2)
        random = RandomForestRegressor(n_estimators=117, random_state=0)
        Price_per_sqft_trainer = random.fit(X_train , Y_train.ravel())
        pickle.dump(Price_per_sqft_trainer ,open("./Main/Random_model.pkl" , 'wb'))
        if self.allow_test == "1":
            return (Price_per_sqft_trainer.score(X_test , Y_test))*100
        else:
            pass

    def knn_predict(self):
        knn_model = pickle.load(open('./Main/knn_model.pkl' , 'rb'))
        return knn_model.predict([[self.area_type,self.availability,self.location,self.size,self.society,self.sqft,self.bath]])


    def random_predict(self):
        random_model = pickle.load(open('./Main/random_model.pkl' , 'rb'))
        return str((random_model.predict([[self.area_type,self.availability,self.location,self.size,self.society,self.sqft,self.bath,self.pps]])[0]))



if __name__ == "__main__":
    test =os.getcwd()
    os.chdir(test)
    obj = Algos()
    obj.knn_model()
    obj.random_model()