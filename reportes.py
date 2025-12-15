import os
import pandas as pd
import matplotlib.pyplot as plt
from colorama import init, Fore
from tabulate import tabulate
from supabase import SupabaseException
from database import conectar
from dotenv import load_dotenv
load_dotenv()
init()

supabase = conectar()

def ver_facturas():
    try:
        datos = supabase.table("facturas").select("*").execute()
        facturas = datos.data

        if not facturas:
            print("No hay facturas registradas.")
            return

        df = pd.DataFrame(facturas)

        os.makedirs("data", exist_ok=True)
        nombre_archivo = "data/reporte_de_facturas.xlsx"
        df.to_excel(nombre_archivo, index=False)

        print(Fore.GREEN + f"Facturas exportadas correctamente a {nombre_archivo}" + Fore.RESET)

    except Exception as e:
        print("Error al exportar facturas:", e)

def reporte_general():
    try:
        datos = supabase.table("facturas").select("tipo_factura,numero,fecha,rnc,cliente,producto,cantidad,monto,itbis,total").execute()
        facturas = datos.data

        if not facturas:
            print("No hay facturas registradas.")
            return

        # DataFrame principal
        df = pd.DataFrame(facturas)

        # ===== RESUMEN GENERAL =====
        total_galones = df["cantidad"].sum()
        total_venta = df["total"].sum()

        resumen = pd.DataFrame({
            "Concepto": ["Total galones vendidos", "Total vendido"],
            "Valor": [total_galones, total_venta]
        })

        # ===== REPORTE POR PRODUCTO =====
        reporte_producto = (
            df.groupby("producto")
              .agg(
                  galones_vendidos=("cantidad", "sum"),
                  total_vendido=("total", "sum")
              )
              .reset_index()
        )
        os.makedirs("data", exist_ok=True)
        nombre_archivo = "data/reporte_general.xlsx"
        with pd.ExcelWriter(nombre_archivo, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Facturas", index=False)
            reporte_producto.to_excel(writer, sheet_name="Ventas por Producto", index=False)
            resumen.to_excel(writer, sheet_name="Resumen General", index=False)

        print(Fore.GREEN + f"Reporte generado correctamente: {nombre_archivo}" + Fore.RESET)

    except Exception as e:
        print("Error al generar reporte:", e)

def grafica_de_productos():
    try:
        datos = supabase.table("facturas").select("producto, cantidad").execute()
        facturas = datos.data

        if not facturas:
            print("No hay datos para graficar.")
            return

        df = pd.DataFrame(facturas)

        # 3. Agrupar por producto y sumar cantidad vendida
        productos_vendidos = df.groupby("producto")["cantidad"].sum()

        # 4. Crear carpeta si no existe
        os.makedirs("data", exist_ok=True)

        # 5. Crear gráfica de barras
        plt.figure(figsize=(8, 5))
        productos_vendidos.plot(kind="bar")
        plt.title("Productos vendidos (Galones)")
        plt.xlabel("Producto")
        plt.ylabel("Galones vendidos")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # 6. Guardar gráfica
        archivo = "data/grafica_productos_vendidos.png"
        plt.savefig(archivo)
        plt.close()

        print(Fore.GREEN + f"Gráfica generada correctamente: {archivo}" + Fore.RESET)

    except Exception as e:
        print("Error al generar la gráfica:", e)


def  menu_reporte():
    while True:
        print("\n-----MENÚ VENTAS-----\n"
            "1. Reporte de facturas\n"
            "2. Reporte general\n"
            "3. Gráfica de ventas por producto\n"
            "4. Salir\n"
        )

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_facturas()
        elif opcion == "2":
            reporte_general()
        elif opcion == "3":
            grafica_de_productos()
        elif opcion == "4":
            break
            
        else:
            print("Opción invalida.\n")
            continue
        return