
# coding: utf-8

# In[43]:


import json, time
from datetime import datetime
from time import mktime
import pickle


from neuralNetwork import NeuralNetwork

## ================================================================

def normalizePrice(price, minimum, maximum):
    return ((2*price - (maximum + minimum)) / (maximum - minimum))

def denormalizePrice(price, minimum, maximum):
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
   
    
    returnData = []
    
    # build items of the form [[average, minimum, maximum], normalized price]
    for i in range(0, len(movingAverages)):
        
        
         
        inputNode = [movingAverages[i], minimums[i], maximums[i]]
        
        price = normalizePrice(values[len(movingAverages) - (i + 1)], minimums[i], maximums[i])
        outputNode = [price]
        tempItem = [inputNode, outputNode]
        
        returnData.append(tempItem)
        
    return returnData

## ================================================================

def getHistoricalData():
    
    historicalPrices = []
    
    
    
    apiData = open('EBL.csv').read().split("\n")

    
    
    for line in apiData:
      
        if(round(len(line) > 0)):
            tempLine = line.split(',')
            
            
            
            
            
            
            
            
            price = float(tempLine[7])
            
            date = tempLine[0]
            
            
            
            
            
            
            historicalPrices.append(price)
            
    return historicalPrices
    
## ================================================================

def getTrainingData():
    
    historicalData = getHistoricalData()
    

    # reverse it so we're using the most recent data first, ensure we only have 9 data points
  
   
    

   
    
    
    # get five 5-day moving averages, 5-day lows, and 5-day highs, associated with the closing price
    trainingData = getTimeSeriesValues(historicalData, 5)
   
    return trainingData


def getPredictionData(value):
    historicalData = getHistoricalData()
    
    # reverse it so we're using the most recent data first, then ensure we only have 5 data points

    
    
    # get five 5-day moving averages, 5-day lows, and 5-day highs
    predictionData = getTimeSeriesValues(historicalData, 5)
   
    # remove associated closing price
    
    predictionData = predictionData[value][0]

    return predictionData





def analyzeSymbol():
   
    
    trainingData = getTrainingData()

    
    network = NeuralNetwork(inputNodes = 3, hiddenNodes = 5, outputNodes = 1)
    
    model = network.train(trainingData)
    
   
    # get rolling data for most recent day
    
    
    predictionData = getPredictionData(0)    
        
        
    returnPrice = network.test(predictionData)
       
        
    predictedStockPrice = denormalizePrice(returnPrice, predictionData[1], predictionData[2])
    returnData = {}
    returnData[0] = predictedStockPrice
        

    return (predictedStockPrice) 
def kiran():
    return ("Mugi")





  





