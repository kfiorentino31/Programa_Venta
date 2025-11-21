import csv
import pandas as pd
from tabulate import tabulate

LISTA_RNC = 'data/RNC.csv'

def limpiar_csv_rnc():
    data_limpia =[]
    
    with open('data/Listado_RNC.csv', 'r', encoding='latin1') as file:
        for linea in file:
            linea = linea.replace(';',',')
            
            data_limpia.append(linea)
    
    with open('data/Listado_RNC_2.csv', 'w', encoding='latin1') as out:
        for linea in data_limpia:
            out.write(linea)


def  ver_clientes():
    
    df = pd.read_csv('data/Listado_RNC_2.csv', encoding='latin1')
    print(tabulate(df, headers='keys', tablefmt='fancy_grid')) # type: ignore



