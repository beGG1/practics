from pprint import pp
from data.data_getter import get_last_val_by_tag
from scipy.stats.stats import mode
from data.data_transformator import parse_contract_to_object, get_variable
from data.data_getter import get_base64, get_model_info
import pandas as pd
import os
from pickle import STRING, loads, load
import base64
import json
import scipy.spatial
from datetime import date
import sklearn
import numpy as np




class C_calculator(object):

    def __init__(self, name, item, tick):
        self.name = name
        self.item = item
        self.tick = tick
        self.data_database = []

    def get_data(self, model_name):
        data = pd.read_csv(model_name + '.csv')
        zip_iterator = zip(data['Unnamed: 0'], data['0'])
        data_new = dict(zip_iterator)
        return data_new
    
    def change_data(self, model_name):
        data = self.item
        indexs_in = []
        #Забираем индексы
        for el_of_data in data:
            indexs_in.append(el_of_data['i'])
        indexs_in.sort()
        #По индексам забираем значения (как-то долго, что перебирает каждый элемент)
        new_data = []
        for el_in in indexs_in:
            for el_of_data in data:
                if el_of_data['i'] == el_in:
                    new_data.append(el_of_data)
        
         #Создаем 2 листа с именами и значениями переменных

        inputs_lst = []
        names_lst = []

        for el in data:
            names_lst.append(el['name'])
            inputs_lst.append(el['points'][0]['v'])

        zip_iterator = zip(names_lst, inputs_lst)
        data_zapr = dict(zip_iterator)
        if model_name == 'GODT_MODEL_DENSITY_BY_VA_A':
            self.data_database['GODT_MODEL_DENSITY_GODT'] = data_zapr['FeedSG_pred']
            self.data_database['GODT:TI11021'] = data_zapr['x__10_65_64_17_GODT_TI11021']
            self.data_database['GODT:PI12119B'] = data_zapr['GODT_PI12119B']
        elif model_name =='MODEL_100A_SN_7_ODT_GODT':
            self.data_database['GODT:TI11129'] = data_zapr['FeedSG_pred']
            self.data_database['GODT:TI11122'] = data_zapr['T_verha']
            self.data_database['LIMS:ONPZ.GODT-10.100A_SN_1_SYRE_BL_A.T95'] = data_zapr['T_niza']
        else:
            return {"result": 123}


    def calculate_prediction(self):
        if self.tick is None:
            tick = False

        self.data_database = self.get_data('GODT_MODEL_DENSITY_BY_VA_A')   
        self.change_data('GODT_MODEL_DENSITY_BY_VA_A')
        inputs_lst = list(self.data_database.values())
        # Загружаем модель? Почему не использовать load, который сразу считывает бинарный?

        with open('GODT_MODEL_DENSITY_BY_VA_A' + '.pickle','rb') as file:
            model_density = load(file)
        
        result_density = model_density.predict(np.array(inputs_lst).reshape(1, -1))

        self.data_database = self.get_data('MODEL_100A_SN_7_ODT_GODT')   
        self.change_data('MODEL_100A_SN_7_ODT_GODT')
        inputs_lst = list(self.data_database.values())

        with open('MODEL_100A_SN_7_ODT_GODT' + '.pickle','rb') as file:
            model_T = load(file)

        result_T = model_T.predict(np.array(inputs_lst).reshape(1, -1))

        return {
            'GODT_MODEL_DENSITY_BY_VA_A': float(result_density),
            'MODEL_100A_SN_7_ODT_GODT': float(result_T)

        }
