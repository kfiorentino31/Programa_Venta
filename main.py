import datetime
from database import conectar
from productos import menu_productos
from lista_clientes import menu_clientes
from Facturas import realizar_venta, ver_facturas
from colorama import init, Fore, Back
from dotenv import load_dotenv

load_dotenv()
conectar()
init()


def main():
    try:
        conectar()
        while True:
            print(Fore.CYAN+"\n==== SISTEMA DE VENTA DE COMBUSTIBLE ====")
            print("\n---PRODUCTOS---\n"
                "1. Venta\n"
                "2. Productos\n"
                "3. Clientes\n"
                "4. Facturas\n"
                "5. Usuarios\n"
                "6. Salir\n")
            
            opcion = input(Fore.CYAN+'Seleccione una opción: '+Fore.RESET)
            
            if opcion == "6":
                print("Cerrando sistema...")
                print("Sistema cerrado")
                break
            
            elif opcion == '1':
                realizar_venta()
            elif opcion == '2':
                menu_productos()
            elif opcion == '3':
                menu_clientes()
            elif opcion == '4':
                ver_facturas()
            elif opcion == '5':
                pass
            else:
                print('Opción invalida. Digite una valida.')
                
    except Exception as ex:
        print("Error: ",ex)

if __name__ == '__main__':
    main()