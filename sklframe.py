# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression


class FastResearchData:
    '''
        load data and change it to the form of dataframe 
    '''
    def __init__(self):
        self.dataset = pd.DataFrame([])

    def loadFromDataFrame(self, df):
        '''
            df = dataframe
        '''
        self.dataset = df
        return self.dataset

    def loadFromCSV(self, address):
        '''
            give the address of csv, load it 
            and transfrom it to dataframe
        '''
        self.dataset = pd.read_csv(address)
        return self.dataset

    def loaddirFromCSV(self, dir):
        '''
            give the dir address, load all csv
        '''
        path = os.getcwd()
        datadir = '/' + args.datadir + '/'
        newdatadir = '/' + args.newdatadir + '/'  # target path

        newdatapath = path + newdatadir
        datapath = path + datadir
        codelist = os.listdir(datapath)  # codelist get

        if not os.path.exists(datapath):
            print('Find error')
        newCodelistlen = []
        for code in codelist:
            with open(datapath + code, 'r') as f:
                readers = csv.reader(f)
                rows = [row for row in readers]
                newCodelistlen.append(len(rows))
                f.close()
        #countMeg = dict(Counter(newCodelistlen))
        #Maxrowlen = sorted(countMeg.items(), key=lambda item: item[1], reverse=True)[0][0]  
        #find the len which has appear more


class IndicatorGallexy:

    def __init__(self, frData):
        self.frData = frData
        self.dataset = frData.copy()

    def getEma(self, span, columnsName): 
        '''
            EMAtoday=α * ( Pricetoday - EMAyesterday ) + EMAyesterday;
        '''      
        alpha = 1.0 * 2 / (span + 1)
        for i in range(len(self.dataset) - 1, -1, -1):
            if i == len(self.dataset) - 1:
                self.dataset.ix[i,'ema'+str(span)]=self.dataset.ix[i,columnsName] 
            else:    
                self.dataset.ix[i,'ema'+str(span)]=(1-alpha)*self.dataset.ix[i+1, columnsName]+alpha*self.dataset.ix[i, columnsName]


    def getAvgPrc(self, columnsName, interval = 10):
        '''
            columnsName(string) the price you want to calculate
            interval(int) is the number to calculate the average

        Returns:
            DataFrame -- the data that add average price as a column
        '''
        for i in range(len(self.dataset) - 1, -1, -1):
            if i > len(self.dataset) - interval:             
                for j in range(i, len(self.dataset)):
                    tmp = 0
                    tmp += self.dataset.ix[j, columnsName]
                    self.frData.ix[i,'AvgPrc'] = tmp
            else:    
                for j in range(i, i + interval):
                    tmp = 0
                    tmp += self.dataset.ix[j, columnsName]
                    self.frData.ix[i,'AvgPrc'] = tmp
        return self.frData

    def getMACD(self, columnsName, span1, span2):
        '''
            EMAtoday=α * Pricetoday + ( 1 - α ) * EMAyesterday
            DIF=EMAtoday（12）－今日today（26）
            MACDtoday=DEAyesterday×8/10+DIFtoday×2/10
            
        Returns:
            DataFrame -- the data that add MACD as a column
        '''
        self.getEma(span1, columnsName)
        self.getEma(span2, columnsName)
        self.dataset['diff'] = self.dataset['ema'+str(span1)] - self.dataset['ema'+str(span2)]
        self.getEma(9, columnsName)
        self.frData['MACD'] = self.dataset['ema9']
        return self.frData




class ModelEngine:
    '''
        prepare for the data
    '''
    
    def __init__(self, dataset, method='SVM', trainingPart=0.9):
        self.method = method
        self.trainingPart = 0.9
        self.dataset = dataset
        self.colHead = dataset.columns.values.tolist()
        self.train_X = 0
        self.train_Y = 0
        self.trainRes = 0
    
    def timeAccess(self):
        '''
        process with time columns

        Returns:
            DataFrame -- the data that the date was split
        '''
        colHead = self.dataset.columns.values.tolist()
        #print colHead
        if 'date' not in colHead:
            print "date is no exit"
            return None
        else:
            date = []
            for no in range(len(self.dataset['date'])):
                date.append(dt.datetime.strptime(self.dataset['date'][no], "%Y-%m-%d %H:%M:%S"))
            date_list = []
            for d in date:
                temp = []
                temp.append(d.year)
                temp.append(d.month)
                temp.append(d.day)
                temp.append(d.hour)
                temp.append(d.minute)
                temp.append(d.second)
                date_list.append(temp)
            #print date_list
            
            del self.dataset['date']
            date_frame = pd.DataFrame(date_list,columns = ['year','month','day','hour','minute','second'])
            #print self.dataset
            result = pd.concat([date_frame,self.dataset],axis = 1)
            

    def setY(self, yname):
        '''
            yname(string): the data you set as y_label
        '''
        if yname in self.colHead:
            col = self.dataset[yname].shift(-1)
            col = col.fillna(0)  #change to dropna
            self.train_Y = np.array(col)
        else:
            yname = yname + "is not exist"
            print (yname)   

    def setX(self, xNameList, yname):
        '''
            xNameList(list): a list that contain all the virable you want to use 
            yname(string): the data you set as y_label
            if xNameList contain yname, than shift yname for one row
        '''
        dfx = pd.DataFrame([])
        if yname in xNameList and yname in self.colHead:
            col = self.dataset[yname].shift(-1)
            col = col.fillna(0)  #change to dropna
            dfx = pd.DataFrame(col)
        else:
            yname = yname + "is not exist"
            print (yname)   
            #exception dealing

        for i in range(0, len(xNameList)):
            if xNameList[i] != yname and xNameList[i] in self.colHead:  
                dfx[str(xNameList[i])] = self.dataset[str(xNameList[i])]
            elif xNameList[i] != yname:
                print (str(xNameList[i]))
                print ("is not exist")

        # print help(skl)
        self.train_X = preprocessing.scale(np.array(dfx))  

    def delX(self, xname):
        '''
            delete the xSeries you don't want
        '''
        colHeadx = self.train_X.columns.values.tolist()
        if xname not in colHeadx:
            print ("cannot find this series in train_X")
        else:
            del self.train_X[xname]


    def train(self, method = 'NN'):
        '''
            input different method and use it to train
        '''
        self.method = method
        if (method == 'LinearRegression'):
            self.trainRes = LinearRegression()

        elif (method == 'LogisticRegression'):
             self.trainRes = LogisticRegression()
        else:
            if (method != 'NN'):
                print ("cannot find this method, use NN")
            self.trainRes = MLPRegressor(hidden_layer_sizes=(50,), activation='relu', solver='adam', 
                alpha=0.0001, batch_size='auto', learning_rate='adaptive', learning_rate_init=0.001)

        self.trainRes = self.trainRes.fit(self.train_X, self.train_Y)
        
    def evaluateOutSample(self):
        '''
            use predict data to predict and give the plot
            plot1 in navy blue is the predict result
            plot2 in red is the train data
            plot3 in orange is creat by counting (train_Y - predict_result) * 10
        '''
        predict_result = []   
        predict_result = self.trainRes.predict(self.train_X)
        plt.hold('on')
        plt.plot(self.dataset.index, predict_result, color= 'navy', label = 'pre_result')
        plt.plot(self.dataset.index, self.train_Y, color= 'red', label = 'train_y')
        plt.plot(self.dataset.index, (self.train_Y - predict_result), color= 'darkorange', label = 'minus')
        
        plt.show()

