

# coding: utf-8

# In[9]:
from datetime import datetime, timedelta

import math
import pickle, csv
import json, time
import sys
import sqlite3 as sql
import json

from datetime import datetime
from time import mktime
from neuralNetwork import NeuralNetwork

## ================================================================

def normalizePrice(price, minimum, maximum):
    #return ((price-minimum)/(maximum-minimum))
    return ((2*price - (maximum + minimum)) / (maximum - minimum))

def denormalizePrice(price, minimum, maximum):
   #return (price*(maximum-minimum) + minimum) 
    return (((price*(maximum-minimum))/2) + (maximum + minimum))/2

## ================================================================

def rollingWindow(seq, windowSize):
    it = iter(seq)
    
    win = [next(it) for cnt in range(windowSize)] # First window
  
    yield win
    
    for e in it: # Subsequent windows
        win[:-1] = win[1:]
        
        win[-1] = e
        yield win
        

def getMovingAverage(values, windowSize):
    
    movingAverages = []
    
    for w in rollingWindow(values, windowSize):
        movingAverages.append(sum(w)/len(w))
    
    return movingAverages

def getMinimums(values, windowSize):
    minimums = []

    for w in rollingWindow(values, windowSize):
        minimums.append(min(w))
            
    return minimums

def getMaximums(values, windowSize):
    maximums = []

    for w in rollingWindow(values, windowSize):
        maximums.append(max(w))

    return maximums

## ================================================================

def getTimeSeriesValues(values, window):
    
    movingAverages = getMovingAverage(values, window)
       
    
    minimums = getMinimums(values, window)
    maximums = getMaximums(values, window)
    length = len(movingAverages)
    
    returnData = []
    
    # build items of the form [[average, minimum, maximum], normalized price]
    for i in range(0, len(movingAverages)):
        
        
         
        inputNode = [movingAverages[i], minimums[i], maximums[i]]  # input node == [3,1,5] | [4.0, 2.0, 6.0] | ....
#        print ("inputNode")
 #       print (inputNode)

        
        #price = normalizePrice(values[i], minimums[i], maximums[i]) 


        price = normalizePrice(values[len(movingAverages) - (i + 1)], minimums[i], maximums[i]) # Why last value ???
        #print (values[len(movingAverages) - (i + 1)])
  #      print ("Price")
        #print (price)
        

        outputNode = [price]
     #   print ("OutputNode")
    #    print(outputNode)
        tempItem = [inputNode, outputNode]
        
        returnData.append(tempItem)
        #print ("Return Data")
        #print (returnData)

    
    return returnData

## ================================================================

def getHistoricalData(name):
    x = name
    historicalPrices = []
    
    
    
    apiData = open('uploads/'+name).read().split("\n")



    
    
    for line in apiData:
        if(round(len(line) > 0)):
            tempLine = line.split(',')
            
       
            
            price = float(tempLine[1])
            
            date = tempLine[0]

           
            historicalPrices.append(price)   # prints the line numbers as [1.0, 2.0, 3.0, 4.0, 5.0, ....]
    
    

            
    return historicalPrices
    
## ================================================================

def getTrainingData(name):
    x=name
    
    historicalData = getHistoricalData(x)
    

    # reverse it so we're using the most recent data first, ensure we only have 9 data points
  
   
    
    # get five 5-day moving averages, 5-day lows, and 5-day highs, associated with the closing price
    trainingData = getTimeSeriesValues(historicalData, 10)


    return trainingData


def getPredictionData(name, a):
    historicalData = getHistoricalData(name)
    
    # reverse it so we're using the most recent data first, then ensure we only have 5 data points

    
    predictionData1 = []
    # get five 5-day moving averages, 5-day lows, and 5-day highs
    predictionData = getTimeSeriesValues(historicalData, 10)
    #print ("predictionData")
    #print (predictionData)
   
    # remove associated closing price
    
    
    predictionData1 = predictionData[a][0]
       

    return predictionData1





def analyzeSymbol(name):
    
    filename = ('uploads/'+name)
    
    count = sum(1 for line in open(filename))



    con = sql.connect("EBL.db")
    cur = con.cursor()
    
    
    y =name
    


    #cur.execute ("DROP TABLE if exists bankname ")
    #cur.execute ('''CREATE TABLE bankname (id INTEGER not null PRIMARY KEY, bankname)''')
#    cur.execute("insert into bankname (bankname) values (?)",  (y,))
    #cur.execute("insert into bankname (name) values (55)")

    con.commit()

   
    


    cur.execute ("DROP TABLE if exists {} ".format (name))





   
    cur.execute( '''CREATE TABLE {}(id INTEGER not null PRIMARY KEY, date DATE, ltp INTEGER, percent INTEGER, high INTEGER, low INTEGER, prediction INTEGER)'''.format(y))
    #cur.execute("CREATE TABLE  fuche ( id INTEGER not null  PRIMARY KEY, date, volume, lamo)")
    with open ('uploads/'+name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
    #print(readCSV)

        
        for row in readCSV:

            
            cur.execute("insert into {} (date, ltp, percent, high, low) values (?,?, ?, ?, ?)".format(y),  ( row[0], row[1], row[2], row[3], row[4]))
            con.commit()
            #b=b+1



#INSERT INTO MyTable(MyIntColumn) VALUES(NULL);
    # cur.execute("insert into {} (date, ltp, percent, high, low) values (NULL, NULL, NULL, NULL, NULL)".format(y))
    # con.commit()



    x = name
    trainingData = getTrainingData(x)


     
    network = NeuralNetwork(inputNodes = 3, hiddenNodes = 2, outputNodes = 1)
    

    network.train(trainingData)


    
    fuckin = []
    pussy = []
    for a in range (0,count-9):
        predictionData = getPredictionData(name, a)    
        
        #returnPrice = loaded_model(network.test(predictionData))
        returnPrice = network.test(predictionData)
        #result = loaded_model.returnPrice
        
        predictedStockPrice = denormalizePrice(returnPrice, predictionData[1], predictionData[2])

        predictedStockPrice=math.floor(predictedStockPrice)
        returnData = {}
        returnData[a] = predictedStockPrice
      

        

        con = sql.connect("EBL.db")
        cur = con.cursor()
        

        

        pussy += [predictedStockPrice]
        #pussy[a]=predictedStockPrice




        
        cur.execute('update {} set prediction = ? WHERE (id = ?)'.format(y), (pussy[a], a+11,)) 
        #cur.execute('insert into fuche (lamo) values (?) WHERE (id = 5)', (returnData[a],)) Working code 
        con.commit()
    


    '''
    for x in range (0,9):
        cur.execute ('SELECT *  FROM plcs WHERE id=(SELECT max(id)-? FROM plcs)', (x,))
        print(x)
        result = cur.fetchall()
        for row in result:
        #print (result)
            print (row[0])
'''


    #cur.execute ('SELECT COUNT(1) from {}'.format(y) )
   # totalrow = cur.fetchone()[0]
#con.commit()
    


    
    
        #cur.execute('UPDATE  fuche set  lamo = "maya" where id = (?)', (a))
        
       # con.commit()
    #print ("Return price")
    #print (returnData['price'])
        #print ("Prediction")
        #conn = sqlite3.connect('EBL.db')
        #curs = conn.cursor()       
        #nm = '2036-12-30'
        #addr = '230'
        #city = '776'
       # curs.execute("INSERT INTO banks (date, value, luck) VALUES (?,?,?)",(nm, addr, returnData[a]) )
       
        #conn.commit()

# to insert the predicted value inside the database
       #print (returnData[a])
   
#            print (b)
    















    


    for bipin in range (0, 9):

        xdata=[]
        for r in range (0,10):
            cur.execute ('SELECT *  FROM {} WHERE id=(SELECT max(id)-? FROM {} )'.format(name, name), (r,))
   # print(a)
            result = cur.fetchall()
            for row in result:
        #print (result)
        #print (row[0])
                data = row[2]
                if data==None:
                    data=row[6]
                xdata.append(data)
        # print (xdata)




        fuckoff = getTimeSeriesValues(xdata, 10)


        fuckin = fuckoff[0][0]
        


        Predicted = network.test(fuckin) 
        predict =   float(denormalizePrice(Predicted, fuckin[1], fuckin[2]))
        predict=math.floor(predict)
        # print ("Predicted")
        # print (predict) 
    

        

        


        cur.execute("SELECT * from {} where id = (SELECT max(id) FROM {})".format(name, name))
        result = cur.fetchall()
        for row in result:
            
            x = row[0]
            print (x)
            datee=row[1]



        # print(row[1]+1)
        # end_date = row[1] + datetime.timedelta(days=10)
        # print (end_date)

            date = datetime.strptime(row[1], "%Y-%m-%d")
            modified_date = date + timedelta(days=1)
            x = datetime.strftime(modified_date, "%Y-%m-%d")
            # print(row[1])



        cur.execute("insert into {} (date, prediction) values (?, ?)".format(name), (x, predict,))
        con.commit()        
    return (returnData[a])

   
     


# In[2]:



# sometime later…


