import csv
import os
import pandas as pd
from tabulate import tabulate
import datetime
from productos import ver_productos


VENTAS_CSV = 'data/facturas.csv'
CAMPOS = ['id','tipo_factura','numero','fecha','rnc','cliente','producto','cantidad','monto','ITBIS','TOTAL']

fecha = datetime.datetime.now()
formato = fecha.strftime("%d/%m/%Y %H:%M:%S")

def inicializar_csv():
    if not os.path.exists(VENTAS_CSV):
        with open(VENTAS_CSV, 'w', newline='', encoding='utf-8') as archivo:
            write = csv.DictWriter(archivo, fieldnames=CAMPOS)
            write.writeheader()
            print(f"Archivo {VENTAS_CSV} creado exitosamente.\n")
        
def obtener_datos():
    datos = []

    try:
        with open(VENTAS_CSV, 'r', newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            
            for fila in reader:
                datos.append(fila)
    except FileNotFoundError:
        print(f'El archivo {VENTAS_CSV} no existe. Valide si el archivo fue borrado o cambiado de ruta.')
    
    return datos

def id_auto(datos):
    if not datos:
        return 1
    
    max_id = max(int(factura['id']) for factura in datos if factura['id'].isdigit())
    
    return max_id + 1


def buscar_producto(codigo):
    try:
        with open('data/productos.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            
            for fila in reader:
                if fila['codigo_producto'] == str(codigo):
                    return fila
                
    except FileNotFoundError:
        print('El archivo de productos.csv no fue encontrado.')
        

def validar_rnc(rnc):
    try:
        with open('data/Listado_RNC.csv','r',encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            
            for fila in reader:
                if fila['RNC'] == str(rnc):
                    return fila
        
    except FileNotFoundError:
        print('El archivo Listado_RNC.csv no fue encontrado.')
    
    return None



def ver_facturas():
    df = pd.read_csv('data/facturas.csv', encoding='utf-8')
    print(tabulate(df, headers='keys', tablefmt='fancy_grid')) # type: ignore
    
    
def venta_rnc():
    inicializar_csv()
    productos = obtener_datos()
    
    while True:
        rnc = input("Ingrese RNC del cliente: ")
        
        if not rnc.isdigit():
            print('Este campo es unicamaente númerico.\n')
            continue
        
        if not (len(rnc) == 9 or len(rnc) == 11):
            print("Debe ingresar exactamente 9 dígitos (RNC) o 11 dígitos (Cédula).\n")
            continue
        
        cliente_data = validar_rnc(rnc)
        
        if cliente_data:
            print(f'Cliente encontrado: {cliente_data['RAZON_SOCIAL']}')
            nombre_cliente = cliente_data['RAZON_SOCIAL']
            break
        else:
            print('RNC no encontrado en la base de datos.')
            return
        
    while True:
        codigo = input('Codfigo de producto: ')
        
        prod = buscar_producto(codigo)
        
        if prod:
            print(f'producto: {prod['producto']}')
            precio = float(prod['precio'])
            break
        else:
            print(f'producto no encontrado o no está registrado.')
        
    monto = float(input('Monto: '))
    cantidad = monto/precio
    
    datos = obtener_datos()
    id_fact = id_auto(datos)
    
    
    factura = {
        'id': id_fact,
        'tipo_factura': 'Con Comprobante Fiscal',
        'numero': f'F-{id_fact}',
        'fecha': formato,
        'rnc': rnc,
        'cliente': nombre_cliente,
        'producto': prod['producto'],
        'cantidad': cantidad,
        'monto' : monto,
        'ITBIS' : 0.00,
        'TOTAL' : monto
    }
        
    with open(VENTAS_CSV, 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS) # type: ignore
        writer.writerow(factura)    

    print(f'\nfactura generada y registrada correctamente.\n')
    
    print("\n----------------------------------------\n"
        "           ESTACION CORAL SRL\n")
    print("**************FACTURA**************\n"
        f"Fecha: {factura['fecha']}\n"
        f"tipo_factura: {factura['tipo_factura']}\n"
        f"NCF: {factura['numero']}\n"
        f"RNC: {factura['rnc']}\n"
        f"Cliente: {factura['cliente']}\n"
        f"\nProducto                     monto\n"
        "------------------------------------\n"
        f"{prod['producto']}............${float(prod['precio']):.2f}\n"
        "\n"
        f"Cantidad....................{float(factura['cantidad']):.2f} Gls.\n"
        f"Subtotal...................${float(factura['monto']):.2f}\n"
        f"ITBIS......................${float(factura['ITBIS']):.2f}\n"
        f"Total.......................${float(factura['TOTAL']):.2f}\n"
        f"*******GRACIAS POR PREFERIRNOS*******\n")
    print("----------------------------------------\n")


def venta_sin_rnc():
    pass


def  realizar_venta():
    while True:
        print("\n-----MENÚ VENTAS-----\n"
            "1. Con Comprobante Fiscal\n"
            "2. Sin Comprobante Fiscal\n"
            "3. Salir\n")
        
        opcion = input('Seleccione el tipo de factura: ')
        
        if opcion == "3":
            print("Facturación cancelada")
            break
        
        elif opcion == '1':
            venta_rnc()
        elif opcion == '2':
            venta_sin_rnc()
            
        else:
            print("Opción invalida.\n")
            continue