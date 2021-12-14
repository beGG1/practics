from typing import List, Optional
from pydantic import BaseModel
# from datetime import date
from fastapi import FastAPI
from fastapi.responses import FileResponse
#from algoritmts.calculator.clalc_funck import calc_f, calc_prognosis, calc_f_st, lol
from algoritmts.calculator.clalc_funck import calculator
from data.data_transformator import parse_contract_to_object, get_variable
from data.data_getter import get_base64, get_model_info
import pandas as pd
import os
from pickle import loads
import base64
import json
import scipy.spatial
from analis.report import PATH_REPORTS
from algoritmts.calculator.C_calculator import C_calculator

class CalcRecomindation(BaseModel):
    name: str
    type_calc: str
    inputs: Optional[list]


class CalcChangeBais(CalcRecomindation):
    tick: bool


app = FastAPI()
@app.post('/calc')
def creat_model(item: CalcRecomindation):
    print('Калькулятор модели рекомендации ')
    calc = calculator(item.name, item.inputs, None)
    #name = item.name
    type_calc = item.type_calc
    print(type_calc)
    # Функция для расчета значений по контракту
    if type_calc == "simple":
        #out = calc_f(name, item)
        out = calc.calc_f()
        print(out)
    elif type_calc == "prognosis":
        print('Функция прогноза активности катализатора')
        #arrayResult = calc_prognosis(name=name, item=item)
        arrayResult = calc.calc_prognosis()
        out = {'result': arrayResult }
    elif type_calc == "simple_static":
        #out = calc_f_st(name, item)
        out = calc.calc_f_st()
        print(out)
    else:
        out = {"result": 123}
        print(out)
    return out


@app.post('/calc_by_tick')
def creat_model(item: CalcChangeBais):
    print('Калькулятор модели рекомендации ')

    calc = calculator(item.name, item.inputs, item.tick)
    #name = item.name
    type_calc = item.type_calc
    #tick = item.tick
    # Функция для расчета значений по контракту
    if type_calc == "simple":
        #out = calc_f(name, item, tick=tick)
        out = calc.calc_f()
        print(out)
    elif type_calc == "prognosis":
        print('Функция прогноза активности катализатора')
        #arrayResult = calc_prognosis(name=name, item=item, tick=tick)
        arrayResult = calc.calc_prognosis()
        out = {'result': arrayResult }
    else:
        out = {"result": 123}
        print(out)
    return out


@app.post('/calculate_prediction')
def create_model(item: CalcRecomindation):
   
    calc = C_calculator(item.name, item.inputs, None)
    type_calc = item.type_calc
    if type_calc == "simple_static":
        #out = calc_f_st(name, item)
        out = calc.calculate_prediction()
        print(out)
    else:
        out = {"result": 123}
        print(out)
    #name = item.name
    #type_calc = item.type_calc
    #tick = item.tick
    return out

@app.get('/model_report')
def get_model_report():
    return FileResponse(f'{PATH_REPORTS}/report_models_of_mks.pdf')

@app.get('/health')
def health_chaek():
    return 'models service is ok!'