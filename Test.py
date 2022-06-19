import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

df = pd.read_excel('Data_Train.xlsx')
df.dropna(inplace=True)

df["Date_of_Journey"] = pd.to_datetime(df["Date_of_Journey"])
# Extract Journey Day & Month
df["Journey_Day"] = df["Date_of_Journey"].dt.day
df["Journey_Month"] = df["Date_of_Journey"].dt.month
df.drop(columns='Date_of_Journey', inplace=True)

# Extract Departure Hour & Minute
df['Dep_Time'] = pd.to_datetime(df['Dep_Time'])
df["Dep_Hour"] = df['Dep_Time'].dt.hour
df["Dep_Minute"] = df['Dep_Time'].dt.minute
df.drop(columns='Dep_Time', inplace=True)

# Extract Arrival Hour & Minute
df['Arrival_Time'] = pd.to_datetime(df["Arrival_Time"])
df['Arrival_hour'] = df['Arrival_Time'].dt.hour
df['Arrival_minute'] = df['Arrival_Time'].dt.minute
df.drop(columns = "Arrival_Time", inplace=True)

# Extract Duration Hour & Minute
duration = list(df["Duration"])
b_min = []
b_hour = []

for i in duration:
    if len(i) > 3:
        s = i.split('m')
        b = s[0].split('h')
        b_min.append(int(b[1].strip()))
        b_hour.append(int(b[0].strip()))
    elif len(i) <= 3:
        if 'm' in i:
            b_min.append(int(i.strip('m')))
            b_hour.append(0)
        elif 'h' in i:
            b_min.append(0)
            b_hour.append(int(i.strip('h')))
df["duration_hour"] = b_hour
df["duration_min"] = b_min
df.drop(columns="Duration", inplace=True)

Airline = pd.get_dummies(df["Airline"], drop_first=True)
source = pd.get_dummies(df["Source"], drop_first=True)
dest = pd.get_dummies(df["Destination"], drop_first=True)
df.drop(columns=["Additional_Info", "Route"], inplace=True)

data = pd.concat([Airline, source, dest, df], axis=1)
data.reset_index(drop=True)

data.drop(columns=["Source","Destination","Airline"],inplace=True)
data.replace({'non-stop':0,'1 stop':1,'2 stops':2,'3 stops':3,'4 stops':4},inplace=True)

x = data.drop(columns="Price")
y = data["Price"]

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2)
rf = RandomForestRegressor()
rf.fit(x_train, y_train)

file = open('flight_pred.pickle',"wb")
pickle.dump(rf , file)







