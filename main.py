from productos import menu_productos
from rnc_contribuyentes import ver_clientes
from Facturas import realizar_venta
from Facturas import ver_facturas
#from clientes import menu_clientes
#from facturas import menu_facturas

def main():
    while True:
        print("\n==== SISTEMA DE VENTA DE COMBUSTIBLE ====")
        print("\n---PRODUCTOS---\n"
            "1. Venta\n"
            "2. Productos\n"
            "3. Clientes\n"
            "4. Facturas\n"
            "5. Usuarios\n"
            "6. Salir\n")
        
        opcion = input('Seleccione una opción: ')
        
        if opcion == "6":
            print("Cerrando sistema...")
            print("Sistema cerrado")
            break
        
        elif opcion == '1':
            realizar_venta()
        elif opcion == '2':
            menu_productos()
        elif opcion == '3':
            ver_clientes()
        elif opcion == '4':
            ver_facturas()
        elif opcion == '5':
            pass
        else:
            print('Opción invalida. Digite una valida.')

if __name__ == '__main__':
    main()
    