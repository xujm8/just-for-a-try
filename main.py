# -*- coding: utf-8 -*-
from sklframe import FastResearchData
from sklframe import IndicatorGallexy
from sklframe import ModelEngine
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'sklframe train and predict the data in 5min')
    parser.add_argument('-d', dest='dataaddress', metavar = 'dataaddress', type=str, nargs='?',
                        help = 'input data dir name (dafault == r"C:\Users\Administrator\Desktop\python\000001.csv")',
                        default = r"C:\Users\Administrator\Desktop\python\000001.csv")

    parser.add_argument('-ty', dest='train_Y', metavar = 'train_Y', type=str, nargs='?',
                        help = 'input the column you want to train(default = price_change)',
                        default = 'price_change')

    parser.add_argument('-m', dest='sklearnmodel', metavar = 'sklearnmodel', type=str, nargs='?',
                        help = 'input the sklearn model you want to train(default = NN)',
                        default = 'NN')
    parser.add_argument('-a', dest='AvgPrc', metavar = 'AvgPrc', type=str, nargs='?',
                        help = 'calculate the average index(default = open)',
                        default = 'open')
    parser.add_argument('-macd', dest='MACD', metavar = 'MACD', type=str, nargs='?',
                        help = 'calculate MACD(default = close)',
                        default = 'close')                    
    args = parser.parse_args()
    #dataset = getDataDB(r"C:\Users\Administrator\Desktop\python\000001.csv")

    #DataFrame并不一定很快，但是很多数据最开始的格式很可能是DataFrame，
    #所以可以用这一步进行预处理，转换为我们内部一个更快格式的数据
    frData= FastResearchData()
    #r"C:\Users\Administrator\Desktop\python\000001.csv"
    frData = frData.loadFromCSV(args.dataaddress)
    # frData.loadFromDataFrame(dataDF)

    # 这里存放了我们的一堆指标计算方法
    # 我们可以将各种指标分成不同的类，以此来管理各种各样的不同分类指标
    xmIG = IndicatorGallexy(frData)
    # rIG = NewTypeOfIndicatorGallexy()
    # x3 = rIG.getNewIND(frData, 'pp')
    frData = xmIG.getAvgPrc(args.AvgPrc, 10)
    frData = xmIG.getMACD(args.MACD, 12, 26)
    # ModelEngine是一个管理训练和评估过程的类
    # 可以在ModelEngine中选择不同的模型，以及不同的训练方法，以及不同的变量
    me = ModelEngine(frData, args.sklearnmodel)
    me.timeAccess()
    me.setX(['price_change', 'ma5', 'ma10', 'ma20', 'v_ma5',
        'v_ma10', 'v_ma20', 'MACD', 'AvgPrc'], args.train_Y)
    me.setY(args.train_Y)
    me.train()
    # 最终可以用Outsample的结果去验证我们模型的好坏
    me.evaluateOutSample()