import pandas as pd
from tabulate import tabulate
from database import conectar
from supabase import SupabaseException
from colorama import init,Fore
import datetime
from dotenv import load_dotenv

load_dotenv()
init()
supabase = conectar()

fecha = datetime.datetime.now()
formato = fecha.strftime("%Y-%m-%d %H:%M:%S")


def buscar_producto(codigo):
    try:
        producto = supabase.table("productos").select("producto, precio").eq("codigo_producto",codigo).execute()
        return producto.data
        
    except SupabaseException as e:
        print("Error: ",e)
        
def secuencia_ncf(prefijo):
    try:
        
        ultimo = (
            supabase.table("facturas")
            .select("numero")
            .like("numero", f"{prefijo}%")
            .order("id", desc=True)
            .limit(1)
            .execute()
        )

        if ultimo.data:
            ncf = ultimo.data[0]["numero"] 
            numero = int(ncf[len(prefijo):])
            return numero + 1
        else:
            return 1

    except Exception as e:
        print("Error al obtener secuencia:", e)
        return 1

    except Exception as e:
        print("Error al obtener secuencia: ", e)
        return 1

def validar_rnc(rnc):
    try:
        cliente = supabase.table("lista_rnc").select("razon_social").eq("rnc",rnc).execute()
        return cliente.data
        
    except SupabaseException as e:
        print("Error: ",e)

def ver_facturas():
    try:
        datos = supabase.table("facturas").select("*").execute()
        df = datos.data

        if not df:
            print("No hay productos registrados.")
            return
        
        print(tabulate(df, headers="keys", tablefmt="fancy_grid")) # type: ignore

    except Exception as e:
        print("Error:", e) # type: ignore
    
    
def venta_con_rnc():   
    while True:
        rnc = input("Ingrese RNC del cliente: ")

        if not (len(rnc) == 9 or len(rnc) == 11):
            print("Debe ingresar exactamente 9 dígitos (RNC) o 11 dígitos (Cédula).\n")
            continue
        
        cliente = validar_rnc(rnc)

        if cliente:
            nombre_cliente = cliente[0]["razon_social"]
            print(f"\nCliente encontrado: {nombre_cliente}\n")
            break
        else:
            print("RNC no encontrado en la base de datos.\n")
            return
        
    while True:
        codigo = input("Código del producto: ")
        producto = buscar_producto(codigo)

        if producto:
            prod_nombre = producto[0]["producto"]
            precio = float(producto[0]["precio"])
            print(f"Producto: {prod_nombre} - Precio: {precio}\n")
            break
        else:
            print("Producto no encontrado.\n")
    
    secuencia = secuencia_ncf("B01")
    monto = float(input('Monto: '))
    cantidad = monto/precio    
    
    factura = supabase.table("facturas").insert({
        'tipo_factura': 'Con Comprobante Fiscal',
        'numero': f'B01{(secuencia):010d}',
        'fecha': formato,
        'rnc': rnc,
        'cliente': nombre_cliente,
        'producto': prod_nombre,
        'cantidad': cantidad,
        'monto' : monto,
        'itbis' : 0.00,
        'total' : monto
    }).execute().data[0]

    print(Fore.GREEN+f'\nfactura generada y registrada correctamente.\n'+Fore.RESET)
    
    print("\n----------------------------------------\n"
        "           ESTACION SRL\n")
    print("**************FACTURA**************\n"
        f"Fecha: {factura['fecha']}\n"
        f"tipo de factura: {factura['tipo_factura']}\n"
        f"NCF: {factura['numero']}\n"
        f"RNC: {factura['rnc']}\n"
        f"Cliente: {factura['cliente']}\n"
        f"\nProducto                     monto\n"
        "------------------------------------\n"
        f"{prod_nombre}............${precio:.2f}\n"
        "\n"
        f"Cantidad....................{cantidad:.2f} Gls.\n"
        f"Subtotal...................${monto:.2f}\n"
        f"ITBIS......................${0.00:.2f}\n"
        f"Total.......................${monto:.2f}\n"
        f"-----------------------------------------\n"
        f"*******GRACIAS POR PREFERIRNOS*******\n")
    print("----------------------------------------\n")
    return


def venta_sin_rnc():
    while True:
        codigo = input("Código del producto: ")
        producto = buscar_producto(codigo)

        if producto:
            prod_nombre = producto[0]["producto"]
            precio = float(producto[0]["precio"])
            print(f"Producto: {prod_nombre} - Precio: {precio}\n")
            break
        else:
            print("Producto no encontrado.\n")
    
    secuencia = secuencia_ncf("B02")
    monto = float(input('Monto: '))
    cantidad = monto/precio    
    
    factura = supabase.table("facturas").insert({
        'tipo_factura': 'Consumidor Final',
        'numero': f'B02{(secuencia):010d}',
        'fecha': formato,
        'rnc': "",
        'cliente': "",
        'producto': prod_nombre,
        'cantidad': cantidad,
        'monto' : monto,
        'itbis' : 0.00,
        'total' : monto
    }).execute().data[0]

    print(Fore.GREEN+f'\nfactura generada y registrada correctamente.\n'+Fore.RESET)
    
    print("\n----------------------------------------\n"
        "           ESTACION SRL\n")
    print("**************FACTURA**************\n"
        f"Fecha: {factura['fecha']}\n"
        f"tipo de factura: {factura['tipo_factura']}\n"
        f"NCF: {factura['numero']}\n"
        f"RNC: {factura['rnc']}\n"
        f"Cliente: {factura['cliente']}\n"
        f"\nProducto                     monto\n"
        "------------------------------------\n"
        f"{prod_nombre}............${precio:.2f}\n"
        "\n"
        f"Cantidad....................{cantidad:.2f} Gls.\n"
        f"Subtotal...................${monto:.2f}\n"
        f"ITBIS......................${0.00:.2f}\n"
        f"Total.......................${monto:.2f}\n"
        f"-----------------------------------------\n"
        f"*******GRACIAS POR PREFERIRNOS*******\n")
    print("----------------------------------------\n")


def  realizar_venta():
    while True:
        print("\n-----MENÚ VENTAS-----\n"
            "1. Con Comprobante Fiscal\n"
            "2. Sin Comprobante Fiscal\n"
            "3. Salir\n")
        
        opcion = input('Seleccione el tipo de factura: ')
        
        if opcion == '1':
            venta_con_rnc()
        elif opcion == '2':
            venta_sin_rnc()
        elif opcion == '3':
            break
            
        else:
            print("Opción invalida.\n")
            continue
        return