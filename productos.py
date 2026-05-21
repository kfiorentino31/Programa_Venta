import os
import pandas as pd
from tabulate import tabulate
from database import conectar
from supabase import SupabaseException
from colorama import init, Fore
init()

try:
    supabase = conectar()
except Exception as e:
    print("Error al conectar a Supabase:", e)
    
def limpiar():
    os.system("cls")
    
class Producto:
    def __init__(self, codigo, nombre, precio, unidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.unidad = unidad

class ProductoCRUD:
    @staticmethod
    def agregar(codigo, nombre, precio, unidad):
        try:
            data = supabase.table("productos").insert({
                "codigo_producto": codigo,
                "producto": nombre,
                "precio": precio,
                "unidad_venta": unidad
            }).execute()

            print(Fore.GREEN + "Producto registrado exitosamente." + Fore.RESET)
            print(data.data)

        except SupabaseException as e:
            print("Error:", e)
    
    @staticmethod
    def listar():
        try:
            datos = supabase.table("productos").select("*").execute()
            df = datos.data

            if not df:
                print("No hay productos registrados.")
                return

            print(tabulate(df, headers="keys", tablefmt="fancy_grid")) # type: ignore

        except SupabaseException as e:
            print("Error:", e)
    
    @staticmethod
    def modificar(codigo, campo, nuevo_valor):
        try:
            data = supabase.table("productos").update({
                campo: nuevo_valor
            }).eq("codigo_producto", codigo).execute()

            print(Fore.GREEN + "Producto actualizado correctamente." + Fore.RESET)
            print(Fore.GREEN + f"{data.data}" + Fore.RESET)

        except SupabaseException as e:
            print("Error:", e)
    
    @staticmethod
    def eliminar(codigo):
        try:
            data = supabase.table("productos").delete().eq("codigo_producto", codigo).execute()

            print(Fore.GREEN + "\nProducto eliminado exitosamente." + Fore.RESET)
            print(Fore.GREEN + f"{data.data}" + Fore.RESET)

        except SupabaseException as e:
            print("Error:", e)

def agregar_producto():
    codigo = input("Código: ")
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))

    unidad = input("Unidad (u/g): ")
    unidad = "Unidad" if unidad == "u" else "Galones" if unidad == "g" else None

    if not unidad:
        print("Unidad inválida.")
        return

    ProductoCRUD.agregar(codigo, nombre, precio, unidad)


def modificar_producto():
    while True:
        print("\n=== MODIFICAR PRODUCTO ===")
        print("1. Modificar precio")
        print("2. Modificar nombre")
        print("3. Modificar código")
        print("4. Volver\n")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            limpiar()
            codigo = input("Código del producto a modificar: ")
            nuevo_precio = float(input("Nuevo precio: "))
            ProductoCRUD.modificar(codigo, "precio", nuevo_precio)
            input("\nPresione Enter para continuar...")
            limpiar()
            return

        elif opcion == "2":
            limpiar()
            codigo = input("Código del producto a modificar: ")
            nuevo_nombre = input("Nuevo nombre del producto: ")
            ProductoCRUD.modificar(codigo, "producto", nuevo_nombre)
            input("\nPresione Enter para continuar...")
            limpiar()
            return

        elif opcion == "3":
            limpiar()
            codigo = input("Código actual del producto: ")
            nuevo_codigo = input("Nuevo código del producto: ")
            ProductoCRUD.modificar(codigo, "codigo_producto", nuevo_codigo)
            input("\nPresione Enter para continuar...")
            limpiar()
            return

        elif opcion == "4":
            limpiar()
            print("Volviendo al menú...")
            limpiar()
            break

        else:
            print("Opción inválida.")


def eliminar_producto():
    codigo = input("Código a eliminar: ")
    ProductoCRUD.eliminar(codigo)

def menu_productos():
    while True:
        print("\n==== MENU PRODUCTOS ====")
        print("1. Lista de productos")
        print("2. Agregar producto")
        print("3. Modificar producto")
        print("4. Eliminar producto")
        print("5. Volver\n")

        opcion = input("Seleccione: ")

        if opcion == "1":
            limpiar()
            ProductoCRUD.listar()
            input("\nPresione Enter para continuar...")
            limpiar()
        elif opcion == "2":
            limpiar()
            agregar_producto()
        elif opcion == "3":
            limpiar()
            modificar_producto()
        elif opcion == "4":
            limpiar()
            eliminar_producto()

        elif opcion == "5":
            limpiar()
            break

        else:
            print("Opción inválida.")