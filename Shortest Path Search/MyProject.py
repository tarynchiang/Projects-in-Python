import requests
import time 
import datetime
import numpy as np
from matplotlib import pyplot as graph


print("Welcome to Bitcoin(BTC) investment program")
print("This is a investing BTC program during specific period")
print(" ")

#get input from users
invest = float(input("How much money would you like to invest in US dollar: "))
period = int(input("How often would you like to check BTC price in second: "))
WholePeriod = float(input("How long would you like to see your investing result in minute: "))
print(" ")

#set variable 
WholePeriod = WholePeriod*60
count = 0
curtime = []
price = []

#get BTC price
def btc():
    BTCprice = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    return BTCprice.json()['bpi']['USD']['rate'] 

#display and save the information into list
curbtc = btc()
print("Price Display:")
print("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()),"in period",period,"s:",curbtc,"USD(initial price)")
curtime = curtime + [datetime.datetime.now()]
price = price + [curbtc.replace(",","")] 
while count < WholePeriod:
    time.sleep(period)
    curbtc = btc()
    print("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()),"in period",period,"s:",curbtc,"USD")
    curtime = curtime + [datetime.datetime.now()]
    price = price + [curbtc.replace(",","")] 
    count += period
		
		
# find the lowest price 
i = 0
Min = price[i]
while i < len(price)-1:
    if Min > price[i+1]:
        Min = price[i+1]
    i+=1
	
# find the highest price
j = 0
Max = price[j]
while j < len(price)-1:
    if Max < price[j+1]:
        Max = price[j+1]
    j+=1

#calculate the average price
i = 0
sum = 0
while i < len(price):
    sum = sum + float(price[i])
    i+=1
AvgMove = sum/WholePeriod

# calculate the earning
iBTC = float(price[0])
fBTC = float(price[len(price)-1])
percentage =(fBTC-iBTC)/iBTC*100
money = invest*(1+percentage)

print("")
print("Highest price", Max,"USD")
print("Lowest price", Min,"USD")
print("the average of price", "{0:0.2f}".format(AvgMove),"USD")
print("Percentage of growth rate","{0:0.1f}".format(percentage),"%")
print("")
if percentage < 0:
	print("you lose", "{0:0.2f}".format(invest-money), "USD")
elif percentage > 0:
	print("Congratulations !!  you earn ","{0:0.2f}".format(money-invest),"USD  in this investment" )
else:
	print("Break even")
	
# do the graph
i= 0
interval = []
while i <= (WholePeriod/period):
    interval += [period*i]
    i+=1

graph.title("the movement of BTC price with time")
graph.ylabel("BTC price")
graph.xlabel("time (sec)")
graph.axes().get_xaxis().set_ticks([])
graph.plot(interval,price)
graph.show()
