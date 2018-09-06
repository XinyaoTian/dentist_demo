# -*-  encoding:utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml import PipelineModel
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class PredictionAnalysis:
    # 初始化函数，建立sparksession以及导入各种模型
    def __init__(self):
        self.curSparkSession = SparkSession.builder.getOrCreate()
        self.vecPipe = PipelineModel.read().load(
            "hdfs://172.17.113.68:9000/user/hadoop/dentistModels/vecAssemblerPipeline")
        self.modelsPipe = PipelineModel.read().load(
            "hdfs://172.17.113.68:9000/user/hadoop/dentistModels/4modelsProcessPipeline")
        self.betterPipe = PipelineModel.read().load(
            "hdfs://172.17.113.68:9000/user/hadoop/dentistModels/GBTBetterRegPipeModel")
        self.wrosePipe = PipelineModel.read().load(
            "hdfs://172.17.113.68:9000/user/hadoop/dentistModels/GBTWroseRegPipeModel")
        logging.info(str(datetime.now()) + "(std time):Class 'prediction_analysis' has been initiated successfully.")

    # 输入一个从字典类型的数据结构，输出处理好的DataFrame
    def dictToDF(self, d):
        typeSchema = StructType(
            [StructField("X1", FloatType()), StructField("X2", FloatType()), StructField("X3", FloatType()),
             StructField("X4", FloatType()),
             StructField("X5", FloatType()), StructField("X6", FloatType()), StructField("X7", FloatType()),
             StructField("X8", FloatType()), StructField("X9", FloatType()), StructField("X10", FloatType()),
             StructField("X11", FloatType())])

        data = (
        [d['X1'], d['X2'], d['X3'], d['X4'], d['X5'], d['X6'], d['X7'], d['X8'], d['X9'], d['X10'], d['X11'], ],)

        logging.info(str(datetime.now()) + "(std time):Inputing dict changed into DF successfully.")
        return self.curSparkSession.createDataFrame(data, schema=typeSchema)

    # 输入一个DF，输出模型预测后有预测值的DF
    def analysisDF(self, dataframe):
        # DF预处理
        df_vecProcessed = self.vecPipe.transform(dataframe)
        # 用融合模型预测Y值
        df_predicted = self.modelsPipe.transform(df_vecProcessed)
        logging.info(str(datetime.now()) + "(std time):Predicting with MERGED model successfully.")
        # 判定Y值是否> = 1
        if df_predicted.select("Y_prediction_gbtc").first()[0] >= 1.0:
            df_better = self.betterPipe.transform(df_predicted)
            logging.info(str(datetime.now()) + "(std time):Predicting with BETTER model successfully.")
            # 若Y >= 1 使用预测治疗结果变好的模型预测Y值
            return df_better
        else:
            df_wrose = self.wrosePipe.transform(df_predicted)
            logging.info(str(datetime.now()) + "(std time):Predicting with WROSE model successfully.")
            # 若Y < 1 使用预测治疗结果变差的模型预测Y值
            return df_wrose

    # 将预测结果转换为dict结构输出
    def resultDFtoDict(self, dataframe):
        result_dict = {}

        # gbtc预测结果及可能性
        result_dict['Y_prediction_gbtc'] = dataframe.select("Y_prediction_gbtc").first()[0]
        result_dict['Y_probability_gbtc'] = dataframe.select("probability").first()[0].values[1]

        # rfc预测结果及可能性
        result_dict['Y_prediction_rfc'] = dataframe.select("Y_prediction_rfc").first()[0]
        result_dict['Y_probability_rfc'] = dataframe.select("probability_rfc").first()[0].values[1]

        # lr预测结果及可能性
        result_dict['Y_prediction_lr'] = dataframe.select("Y_prediction_lr").first()[0]
        result_dict['Y_probability_lr'] = dataframe.select("probability_lr").first()[0].values[1]

        # svc预测结果及可能性
        result_dict['Y_prediction_svc'] = dataframe.select("Y_prediction_svc").first()[0]

        # gbtr预测结果及可能性
        result_dict['Y_prediction_gbtreg'] = dataframe.select("Y_prediction_gbtreg").first()[0]

        return result_dict

    # 将上面的三个函数串起来，变为预测处理函数
    # 输入：dict 输出：有预测值的dict
    def analysisData(self, dictData):
        df = self.dictToDF(dictData)
        dfWithResult = self.analysisDF(df)
        dictWithResult = self.resultDFtoDict(dfWithResult)
        return dictWithResult

    # 将上面的三个函数串起来，变为预测处理函数,并将格式转换为供前端界面显示的类型
    # 输入：dict 输出：有预测值的dict
    def analysisData_webOutput(self, dictData):
        df = self.dictToDF(dictData)
        dfWithResult = self.analysisDF(df)
        dictWithResult = self.resultDFtoDict(dfWithResult)
        dictWithResult['Y_probability_lr'] = int(dictWithResult['Y_probability_lr'] * 10000) * 0.01
        dictWithResult['Y_probability_svc'] = int(dictWithResult['Y_prediction_svc'] * 10000) * 0.01
        dictWithResult['Y_probability_rfc'] = int(dictWithResult['Y_probability_rfc'] * 10000) * 0.01
        dictWithResult['Y_probability_gbtc'] = int(dictWithResult['Y_probability_gbtc'] * 10000) * 0.01
        dictWithResult['Y_prediction_gbtreg'] = int(dictWithResult['Y_prediction_gbtreg'] * 100) * 0.01
        return dictWithResult


