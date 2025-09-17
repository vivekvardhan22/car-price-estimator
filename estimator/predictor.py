import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
location = os.path.join(base_dir, "data","car_prices.csv")
data_v1 = pd.read_csv(location)

#deleting rows which contain empty values
data_v1=data_v1.drop(columns=["mmr","vin"])
data_v1=data_v1.dropna(subset=["saledate","sellingprice","interior","color","odometer","make","model","trim","body","condition","transmission"])



#edited saledate coulmn and made it in datetime format
data_v1["saledate"] = data_v1["saledate"].str.replace("(PST)","")
data_v1["saledate"] = data_v1["saledate"].str.replace("(PDT)","")
data_v1["saledate"] = data_v1["saledate"].str.replace("GMT-0800 ","")
data_v1["saledate"] = data_v1["saledate"].str.replace("GMT-0700 ","")
data_v1["saledate"] = data_v1["saledate"].str.replace("Mon","")
data_v1["saledate"] = data_v1["saledate"].str.replace("Tue","")
data_v1["saledate"] = data_v1["saledate"].str.replace("Wed","")
data_v1["saledate"] = data_v1["saledate"].str.replace("Thu","")
data_v1["saledate"] = data_v1["saledate"].str.replace("Fri","")
data_v1["saledate"] = data_v1["saledate"].str.replace("Sat","")
data_v1["saledate"] = data_v1["saledate"].str.replace("Sun","")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Jan ","01/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Feb ","02/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Mar ","03/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Apr ","04/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" May ","05/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Jun ","06/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Jul ","07/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Aug ","08/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Sept ","09/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Oct ","10/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Nov ","11/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" Dec ","12/")
data_v1["saledate"] = data_v1["saledate"].str.replace(" 2013","/2013")
data_v1["saledate"] = data_v1["saledate"].str.replace(" 2014","/2014")
data_v1["saledate"] = data_v1["saledate"].str.replace(" 2015","/2015")
data_v1["saledate"] = data_v1["saledate"].str.strip()
data_v1["saledate"] = pd.to_datetime(data_v1["saledate"], format='%m/%d/%Y %H:%M:%S', dayfirst=False)
data_v1["age"] =  data_v1["saledate"].dt.year - data_v1["year"] 

#edited age column and removed negative age rows
i = data_v1[(data_v1["age"]<0)].index
data_v1.drop(i, inplace=True)


#adding a variable called authorized seller grading 0|1 on the basis of seller
rating = [1,0]
auth_sell = "Kia|kia|^wells|^zip|honda|ford|chevrolet|dodge|jeep|gmc|buick|chrysler|nissan|ram|hyundai|toyota|subaru|mazda|volkswagen|mitsubishi|lincoln|cadillac|acura|infiniti|lexus|mini|MINI|mercedes-benz|bmw|audi|volvo"
condition = [data_v1["seller"].str.contains(auth_sell), ~data_v1["seller"].str.contains(auth_sell)]
data_v1["seller_rating"] = np.select(condition, rating, default=0)


#adding a variable called reliability grading 0|1|2 on the basis of brand
long_run = [2,1,0]
high_rel = "^Toyota|^toyota|Benz|benz|Lexus|lexus|Jeep|jeep|Dod|BMW|Mini|MINI|GMC|gmc|Fiat|Cadillac|cadillac|^Chev|^chev|^Lin|^lin|^Audi|^audi|^Mitsu|^mitsu|^Volvo|^volvo|^Volks|^volks|^Land|^land|^Jag|^jag|^Hon|^hon|^Por|^por|^Humm|^humm|^Isu|^isu|^Mase|^mase|^Ben|^beb|^Ast|^ast|^Ferr|^ferr|^Roll|^roll|^Lambo|^lambo|^Ford|^ford|^Buick|^buick|^Kia|^kia|^Subaru|^subaru|^Mazda|^mazda|^Hyundai|^hyundai"
med_rel = "^Tesla|^tesla|^Nissan|^nissan|^Chrysler|^chrysler|Acura|Scion|Suzu"
low_rel = "Inf|Ram|Pon|Sat|Mer|Saab|Smart|Old|Poly|Geo|Fis|Dae|Lotus"
condition_2 = [data_v1["make"].str.contains(high_rel), data_v1["make"].str.contains(med_rel), data_v1["make"].str.contains(low_rel)]
data_v1["reliability"] = np.select(condition_2, long_run, default=0)


#proving hypothesis 1
#sns.scatterplot(data=data_v1, x="reliability", y="sellingprice",hue="seller_rating")
#plt.show()
#plt.savefig("expected_sell_price/data/reliability_sellingprice_sellerrating.jpg")


#proving hypothesis 2
#sns.scatterplot(data=data_v1, x="odometer", y="sellingprice", hue="seller_rating")
#plt.ticklabel_format(style='plain', axis='x')
#plt.show()
#plt.savefig("expected_sell_price/data/odometer_sellingprice_sellerrating.jpg")

#proving hypothesis 3
#sns.scatterplot(data=data_v1, x="age", y="sellingprice", hue="reliability")
#plt.show()
#plt.savefig("expected_sell_price/data/age_sellingprice_reliability.jpg")



#Giving points based on model pref and selling price
bins=[1]*53
condition_4 = [
   (data_v1["make"]=="Audi") & (data_v1["sellingprice"]> 1.0*(np.std(data_v1[data_v1["make"]=="Audi"]["sellingprice"]))),
   (data_v1["make"]=="Kia") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Kia"]["sellingprice"]))),
   (data_v1["make"]=="Toyota") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Toyota"]["sellingprice"]))),
   (data_v1["make"]=="Ford") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Ford"]["sellingprice"]))),
   (data_v1["make"]=="Chevrolet") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Chevrolet"]["sellingprice"]))),
   (data_v1["make"]=="Honda") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Honda"]["sellingprice"]))),
   (data_v1["make"]=="Nissan") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Nissan"]["sellingprice"]))),
   (data_v1["make"]=="Subaru") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Subaru"]["sellingprice"]))),
   (data_v1["make"]=="Hyundai") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Hyundai"]["sellingprice"]))),
   (data_v1["make"]=="Mazda") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Mazda"]["sellingprice"]))),
   (data_v1["make"]=="Volkswagen") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Volkswagen"]["sellingprice"]))),
   (data_v1["make"]=="Dodge") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Dodge"]["sellingprice"]))),
   (data_v1["make"]=="GMC") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="GMC"]["sellingprice"]))),
   (data_v1["make"]=="Jeep") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Jeep"]["sellingprice"]))),
   (data_v1["make"]=="Buick") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Buick"]["sellingprice"]))),
   (data_v1["make"]=="Cadillac") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Cadillac"]["sellingprice"]))),
   (data_v1["make"]=="Chrysler") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Chrysler"]["sellingprice"]))),
   (data_v1["make"]=="Ram") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Ram"]["sellingprice"]))),
   (data_v1["make"]=="BMW") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="BMW"]["sellingprice"]))),
   (data_v1["make"]=="Mercedes-Benz") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Mercedes-Benz"]["sellingprice"]))),
   (data_v1["make"]=="Lexus") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Lexus"]["sellingprice"]))),
   (data_v1["make"]=="Infiniti") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Infiniti"]["sellingprice"]))),
   (data_v1["make"]=="Acura") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Acura"]["sellingprice"]))),
   (data_v1["make"]=="Mini") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Mini"]["sellingprice"]))),
   (data_v1["make"]=="Volvo") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Volvo"]["sellingprice"]))),
   (data_v1["make"]=="Mitsubishi") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Mitsubishi"]["sellingprice"]))),
   (data_v1["make"]=="Lincoln") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Lincoln"]["sellingprice"]))),
   (data_v1["make"]=="Pontiac") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Pontiac"]["sellingprice"]))),
   (data_v1["make"]=="Saturn") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Saturn"]["sellingprice"]))),
   (data_v1["make"]=="Saab") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Saab"]["sellingprice"]))),
   (data_v1["make"]=="Tesla") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Tesla"]["sellingprice"]))),
   (data_v1["make"]=="Mercury") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Mercury"]["sellingprice"]))),
   (data_v1["make"]=="Hummer") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Hummer"]["sellingprice"]))),
   (data_v1["make"]=="Land Rover") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Land Rover"]["sellingprice"]))),
   (data_v1["make"]=="Jaguar") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Jaguar"]["sellingprice"]))),
   (data_v1["make"]=="Porsche") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Porsche"]["sellingprice"]))),
   (data_v1["make"]=="Ferrari") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Ferrari"]["sellingprice"]))),
   (data_v1["make"]=="Lamborghini") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Lamborghini"]["sellingprice"]))),
   (data_v1["make"]=="Scion") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Scion"]["sellingprice"]))),
   (data_v1["make"]=="Suzuki") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Suzuki"]["sellingprice"]))),
   (data_v1["make"]=="Fiat") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Fiat"]["sellingprice"]))),
   (data_v1["make"]=="smart") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="smart"]["sellingprice"]))),
   (data_v1["make"]=="Oldsmobile") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Oldsmobile"]["sellingprice"]))),
   (data_v1["make"]=="Isuzu") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Isuzu"]["sellingprice"]))),
   (data_v1["make"]=="Maserati") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Maserati"]["sellingprice"]))),
   (data_v1["make"]=="Aston Martin") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Aston Martin"]["sellingprice"]))),
   (data_v1["make"]=="Bentley") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Bentley"]["sellingprice"]))),
   (data_v1["make"]=="Rolls-Royce") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Rolls-Royce"]["sellingprice"]))),
   (data_v1["make"]=="Polymouth") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Polymouth"]["sellingprice"]))),
   (data_v1["make"]=="Geo") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Geo"]["sellingprice"]))),
   (data_v1["make"]=="Fisker") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Fisker"]["sellingprice"]))),
   (data_v1["make"]=="Daewoo") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Daewoo"]["sellingprice"]))),
   (data_v1["make"]=="Lotus") & (data_v1["sellingprice"] > 1.0*(np.std(data_v1[data_v1["make"]=="Lotus"]["sellingprice"]))),
]
data_v1["model_rating"] = np.select(condition_4, bins, default=0)


#function to predict the price
def predict(company,variant,seller_auth,odometer_reading,car_purchase_year):
    high_rel_list = ["Toyota","Mercedes-Benz","Lexus","Jeep","Dodge","BMW","Mini","MINI","GMC","Fiat","Cadillac","Chevrolet","Lincoln","Audi","Mitsubishi","Volvo","Volkswagen","Land Rover","Jaguar","Honda","Porsche","Hummer","Isuzu","Maserati","Bentley","Aston Martin","Rolls-Royce","Ferrari","Lamborghini","Ford","Buick","Kia","Subaru","Mazda","Hyundai"]
    med_rel_list = ["Tesla","Nissan","Chrysler","Acura","Scion","Suzuki"]
    low_rel_list = ["Infiniti","Ram","Pontiac","Saturn","Mercury","Saab","Smart","Oldsmobile","Polymouth","Geo","Fisker","Daewoo","Lotus"]
    
    if company in high_rel_list:
         reliability = 2
    elif company in med_rel_list:
         reliability = 1
    elif company in low_rel_list:
       reliability = 0
    else:
       reliability = 0
       
   #for min price
    min = np.max(data_v1.loc[(data_v1["make"]==company) & (data_v1["model"]==variant) & (data_v1["seller_rating"]==seller_auth) & (data_v1["reliability"]>=reliability) & (data_v1["model_rating"]==0)]["sellingprice"])
    min_2 = np.min(data_v1.loc[(data_v1["make"]==company) & (data_v1["model"]==variant) & (data_v1["seller_rating"]==seller_auth) & (data_v1["reliability"]>=reliability) & (data_v1["model_rating"]==1)]["sellingprice"])
   
   #for max price
    max = np.max(data_v1.loc[(data_v1["make"]==company) & (data_v1["model"]==variant) & (data_v1["seller_rating"]==seller_auth) & (data_v1["reliability"]>=reliability) & (data_v1["model_rating"]==1)]["sellingprice"])
    max_2 = np.max(data_v1.loc[(data_v1["make"]==company) & (data_v1["model"]==variant) & (data_v1["seller_rating"]==seller_auth) & (data_v1["reliability"]>=reliability) & (data_v1["model_rating"]==0)]["sellingprice"])
    
    if min < min_2:
       min = min
    else:
       min = min_2
    
    if max > max_2:
       max = max 
    else:
       max = max_2
    
    if odometer_reading >= 95000:
       min = min - 1000
       max = max - 1000
    else:
       min = min
       max = max
    
    if (2025 - car_purchase_year) >= 9:
         min = min - 800
         max = max - 800
    else:
         min = min
         max = max
         
    #print(f"The expected selling price of your car is between ${min} and ${max}")
    return min,max







"""print("Welcome to the car price predictor!\n")
print("Please enter the following details about the car:\n")
print(f"Choose the car company from the list {data_v1["make"].unique()}\n")
com = input("Enter the car company: ")
print("\n")
if com not in data_v1["make"].unique():
      print("Company not found in the database. Please try again.\n")
      com = input("Enter the car company: ")
      print("\n")
print(f"Choose the car model from the list {data_v1[data_v1["make"]==com]["model"].unique()}\n")
var = input("Enter the car model again: ")
print("\n")
if var not in data_v1[data_v1["make"]==com]["model"].unique():
      print("Model not found in the database. Please try again.\n")
      var = input("Enter the car model again: ")
      print("\n")
print("If the seller is an authorized dealer type 1 else type 0\n")
auth = int(input("Enter 1 or 0: "))
print("please enter the Odometer reading of the car (in miles)")
odo = int(input("Enter the odometer reading: "))
print("\n")
print("Please enter the year in which you purchased the car\n")
year = int(input("Enter the purchase year: "))
print("\n")
predict(com,var,auth,odo,year)"""
