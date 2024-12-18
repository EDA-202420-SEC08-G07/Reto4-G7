import sys
import App.logic as logic
import time
import csv
import sys
import os
import json
from tabulate import tabulate


def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control  

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
def load_data(control, data_dir):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    nombre_archivo_usuarios = input("Ingrese el nombre del archivo de usuarios ('users_info_large.csv'): ")
    nombre_archivo_relaciones = input("Ingrese el nombre del archivo de las relaciones ('relationships_large.csv'): ")
    catalog =logic.load_data(control, data_dir, nombre_archivo_usuarios, nombre_archivo_relaciones)
    total_usuarios, total_conexiones, usuarios_basic, usuarios_premium, promedio_seguidores, ciudad_mayor, max_usuarios = logic.report_data(catalog)
    print(f"Número total de usuarios: {total_usuarios}")
    print(f"Número total de conexiones: {total_conexiones}")
    print(f"Número de usuarios Basic: {usuarios_basic}")
    print(f"Número de usuarios Premium: {usuarios_premium}")
    print(f"Número promedio de seguidores por usuario: {promedio_seguidores:.2f}")
    print(f"Ciudad con mayor número de usuarios: {ciudad_mayor} ({max_usuarios} usuarios)")
    return catalog


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    usuario_a = input("ingrese el id del usuario a: ")
    usuario_b = input("ingrese el id del usuario b: ")
    start_time = logic.get_time()
    total, camino = logic.req_1(control, usuario_a, usuario_b)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if total is not None:
        print(f'Si hay un camino entre el usuario {usuario_a} y el usuario {usuario_b}')
        print(f'El total de conexiones es de {total}')
        print('El camino es: ')
        for Id, alias, type_user in camino:
            print(f"ID: {Id}, Alias: {alias}, Tipo de Usuario: {type_user}")
    else:
        print(f"No se encontró un camino entre el usuario {usuario_a} y el usuario {usuario_b}.")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    usuario_a = input("ingrese el id del usuario a: ")
    usuario_b = input("ingrese el id del usuario b: ")
    start_time = logic.get_time()
    total, camino = logic.req_2(control, usuario_a, usuario_b)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if total=="PREMIUM":
        print("ERROR")
        print(f'El usuario {usuario_a} es PREMIUM')
        print(f'El usuario {usuario_b} es PREMIUM')
    elif total is not None:
        print(f'Si hay un camino entre el usuario {usuario_a} y el usuario {usuario_b}')
        print(f'El total de conexiones es de {total}')
        print('El camino es: ')
        for id, alias, tipo_usuario in camino:
            print(f"ID: {id}, Alias: {alias}, Tipo de Usuario: {tipo_usuario}")
    else:
        print(f"No se encontró un camino entre el usuario {usuario_a} y el usuario {usuario_b}.")


def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    user_id = input('Ingrese el ID del usuario al cual desea averiguar su amigo con más seguidores: ')
    resultado = logic.req_3(control, user_id)
    tiempo = resultado[0]
    amigo_popular = resultado[1]
    max_seguidores = resultado[2]

    print(f'El tiempo del algoritmo fue {tiempo} ms')

    if amigo_popular:
        table = tabulate(
            [[amigo_popular['id'], amigo_popular['alias'], amigo_popular['tipo'], amigo_popular['seguidores']]],
            headers=['ID', 'Alias', 'Tipo', 'Seguidores'],
            tablefmt='grid'
        )
        print(f'\nEl amigo más popular del usuario {user_id} según su cantidad de seguidores es:')
        print(table)
        print(f'\nLa cantidad total de seguidores del amigo más popular es: {max_seguidores}')
    else:
        print(f'\nEl usuario {user_id} no tiene amigos o no se encontró un amigo más popular.')


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    usuario_a = input("ingrese el id del usuario a: ")
    usuario_b = input("ingrese el id del usuario b: ")
    start_time = logic.get_time()
    lista=logic.req_4(control, usuario_a, usuario_b)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if lista is not None:
        print('La lista de los amigos en comun es de: ')
        for id, alias, type_user in lista:
            print(f"ID: {id}, Alias: {alias}, Tipo de Usuario: {type_user}")
    else:
        print(f"No se encontraron amigos en comun entre el usuario {usuario_a} y el usuario {usuario_b}.")


def print_req_5(control):
    """
    Función que imprime la solución del Requerimiento 5 en consola.
    """
    usuario_a = input("Ingrese el ID del usuario: ")
    n = int(input("Ingrese la cantidad de amigos que siguen a más usuarios (N): "))
    start_time = logic.get_time()
    amigos_ordenados = logic.req_5(control, usuario_a, n)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if amigos_ordenados:
        print(f"\nLos {n} amigos que siguen a más usuarios en la red son:\n")
        for amigo in amigos_ordenados:
            print(f"ID: {amigo['id']}, Alias: {amigo['alias']}, Seguidos: {amigo['seguidos']}")
    else:
        print(f"No se encontraron amigos para el usuario con ID {usuario_a}.")


def print_req_6(control):
    """
    Imprime la solución del Requerimiento 6 en consola.
    """
    N = int(input("Ingrese el número de usuarios más populares que desea consultar (N >= 2): "))
    if N < 2:
        print("El número de usuarios debe ser al menos 2.")
        return
    start_time = logic.get_time()
    top_users, arbol = logic.req_6(control, N)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    print(f"\nLos {N} usuarios más populares:")
    for user in top_users:
        print(f"ID: {user['id']}, Alias: {user['alias']}, Seguidores: {user['seguidores']}")
    if arbol:
        print("\nÁrbol que conecta a los usuarios más populares:")
        for key in bst.key_set(arbol)["elements"]:
            print(f"Nodo: {key}")
    else:
        print("No se pudo conectar a todos los usuarios en un árbol.")




def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    usuario_a = input("Ingrese el ID del usuario: ")
    lista_hobbies = input("Ingrese los hobbies de los cuales desea conocer la subred: ")
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    lista_hobbies = lista_hobbies.split(",")
    for i in range(len(lista_hobbies)):
        lista_hobbies[i] = lista_hobbies[i].strip()
    start_time = logic.get_time()
    directos, indirectos, cantidad, lista_amigos=logic.req_7(control, usuario_a, lista_hobbies)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if len(lista_amigos)!=0:
        print("El total de amigos con intereses en comun es de: ", cantidad)
        print(f"Tiene un total de {directos} amigos directos y {indirectos} amigos indirectos")
        print("La subred de amigos encontrada es la siguiente: ")
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
        for grado, amigo, lista, comun in lista_amigos:
            if comun:
                print(f"El usuario tiene una profundidad de: {grado}, id: {amigo}, y tiene la siguiente lista de hobbies: {lista} y tienen los siguientes hobbies con el usuario buscado: {comun}")
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
            else:
                print(f"El usuario tiene una profundidad de: {grado}, id: {amigo}, y tiene la siguiente lista de hobbies: {lista} pero no tienen ningun hobbie en comun con el usuario buscado")
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
    else:
        print("No se encontraron amigos con los mismos intereses")


def print_req_8(control):
    """
    Función que imprime la solución del Requerimiento 8 en consola.
    Permite graficar en un mapa los usuarios dentro de un radio dado desde unas coordenadas específicas.
    """
    center_lat = float(input("Ingrese la latitud del centro: "))
    center_lon = float(input("Ingrese la longitud del centro: "))
    radius_km = float(input("Ingrese el radio en kilómetros: "))

    resultado = logic.req_8(control, center_lat, center_lon, radius_km)
    mapa = resultado[0]
    tiempo = resultado[1]

    # Guardamos el mapa en un archivo HTML
    file_name = "usuarios_mapa.html"
    mapa.save(file_name)
    
    print(f'El tiempo del algoritmo fue {tiempo} ms')
    print(f"El mapa ha sido generado exitosamente y guardado como '{file_name}'.")
    print(f"Abra el archivo '{file_name}' en su navegador para visualizar el mapa interactivo.")
    #IMPORTANTE El archivo usuarios_mapa.html se guardará en el mismo directorio donde se está ejecutando el codigo de Python.


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control, data_dir)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

import sys
import App.logic as logic
import time
import csv
import sys
import os
import json
from tabulate import tabulate
from DataStructures.Tree import binary_search_tree as bst


def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control  

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
def load_data(control, data_dir):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    nombre_archivo_usuarios = input("Ingrese el nombre del archivo de usuarios ('users_info_large.csv'): ")
    nombre_archivo_relaciones = input("Ingrese el nombre del archivo de las relaciones ('relationships_large.csv'): ")
    catalog =logic.load_data(control, data_dir, nombre_archivo_usuarios, nombre_archivo_relaciones)
    total_usuarios, total_conexiones, usuarios_basic, usuarios_premium, promedio_seguidores, ciudad_mayor, max_usuarios = logic.report_data(catalog)
    print(f"Número total de usuarios: {total_usuarios}")
    print(f"Número total de conexiones: {total_conexiones}")
    print(f"Número de usuarios Basic: {usuarios_basic}")
    print(f"Número de usuarios Premium: {usuarios_premium}")
    print(f"Número promedio de seguidores por usuario: {promedio_seguidores:.2f}")
    print(f"Ciudad con mayor número de usuarios: {ciudad_mayor} ({max_usuarios} usuarios)")
    return catalog


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    usuario_a = input("ingrese el id del usuario a: ")
    usuario_b = input("ingrese el id del usuario b: ")
    start_time = logic.get_time()
    total, camino = logic.req_1(control, usuario_a, usuario_b)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if total is not None:
        print(f'Si hay un camino entre el usuario {usuario_a} y el usuario {usuario_b}')
        print(f'El total de conexiones es de {total}')
        print('El camino es: ')
        for Id, alias, type_user in camino:
            print(f"ID: {Id}, Alias: {alias}, Tipo de Usuario: {type_user}")
    else:
        print(f"No se encontró un camino entre el usuario {usuario_a} y el usuario {usuario_b}.")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    usuario_a = input("ingrese el id del usuario a: ")
    usuario_b = input("ingrese el id del usuario b: ")
    start_time = logic.get_time()
    total, camino = logic.req_2(control, usuario_a, usuario_b)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if total=="PREMIUM":
        print("ERROR")
        print(f'El usuario {usuario_a} es PREMIUM')
        print(f'El usuario {usuario_b} es PREMIUM')
    elif total is not None:
        print(f'Si hay un camino entre el usuario {usuario_a} y el usuario {usuario_b}')
        print(f'El total de conexiones es de {total}')
        print('El camino es: ')
        for id, alias, tipo_usuario in camino:
            print(f"ID: {id}, Alias: {alias}, Tipo de Usuario: {tipo_usuario}")
    else:
        print(f"No se encontró un camino entre el usuario {usuario_a} y el usuario {usuario_b}.")


def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    user_id = input('Ingrese el ID del usuario al cual desea averiguar su amigo con más seguidores: ')
    resultado = logic.req_3(control, user_id)
    tiempo = resultado[0]
    amigo_popular = resultado[1]
    max_seguidores = resultado[2]

    print(f'El tiempo del algoritmo fue {tiempo} ms')

    if amigo_popular:
        table = tabulate(
            [[amigo_popular['id'], amigo_popular['alias'], amigo_popular['tipo'], amigo_popular['seguidores']]],
            headers=['ID', 'Alias', 'Tipo', 'Seguidores'],
            tablefmt='grid'
        )
        print(f'\nEl amigo más popular del usuario {user_id} según su cantidad de seguidores es:')
        print(table)
        print(f'\nLa cantidad total de seguidores del amigo más popular es: {max_seguidores}')
    else:
        print(f'\nEl usuario {user_id} no tiene amigos o no se encontró un amigo más popular.')


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    usuario_a = input("ingrese el id del usuario a: ")
    usuario_b = input("ingrese el id del usuario b: ")
    start_time = logic.get_time()
    lista=logic.req_4(control, usuario_a, usuario_b)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if lista is not None:
        print('La lista de los amigos en comun es de: ')
        for id, alias, type_user in lista:
            print(f"ID: {id}, Alias: {alias}, Tipo de Usuario: {type_user}")
    else:
        print(f"No se encontraron amigos en comun entre el usuario {usuario_a} y el usuario {usuario_b}.")


def print_req_5(control):
    """
    Función que imprime la solución del Requerimiento 5 en consola.
    """
    usuario_a = input("Ingrese el ID del usuario: ")
    n = int(input("Ingrese la cantidad de amigos que siguen a más usuarios (N): "))
    start_time = logic.get_time()
    amigos_ordenados = logic.req_5(control, usuario_a, n)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if amigos_ordenados:
        print(f"\nLos {n} amigos que siguen a más usuarios en la red son:\n")
        for amigo in amigos_ordenados:
            print(f"ID: {amigo['id']}, Alias: {amigo['alias']}, Seguidos: {amigo['seguidos']}")
    else:
        print(f"No se encontraron amigos para el usuario con ID {usuario_a}.")


def print_req_6(control):
    """
    Imprime la solución del Requerimiento 6 en consola.
    """
    N = int(input("Ingrese el número de usuarios más populares que desea consultar (N >= 2): "))
    if N < 2:
        print("El número de usuarios debe ser al menos 2.")
        return
    start_time = logic.get_time()
    top_users, arbol = logic.req_6(control, N)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    print(f"\nLos {N} usuarios más populares:")
    for user in top_users:
        print(f"ID: {user['id']}, Alias: {user['alias']}, Seguidores: {user['seguidores']}")
    if arbol:
        print("\nÁrbol que conecta a los usuarios más populares:")
        for key in bst.key_set(arbol)["elements"]:
            print(f"Nodo: {key}")
    else:
        print("No se pudo conectar a todos los usuarios en un árbol.")




def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    usuario_a = input("Ingrese el ID del usuario: ")
    lista_hobbies = input("Ingrese los hobbies de los cuales desea conocer la subred: ")
    print("--------------------------------------------------------------------------------------------------------------------------------------------")
    lista_hobbies = lista_hobbies.split(",")
    for i in range(len(lista_hobbies)):
        lista_hobbies[i] = lista_hobbies[i].strip()
    start_time = logic.get_time()
    directos, indirectos, cantidad, lista_amigos=logic.req_7(control, usuario_a, lista_hobbies)
    end_time = logic.get_time()
    elapsed_time = logic.delta_time(start_time, end_time)
    print(f"El tiempo de ejecución fue: {elapsed_time} ms")
    if len(lista_amigos)!=0:
        print("El total de amigos con intereses en comun es de: ", cantidad)
        print(f"Tiene un total de {directos} amigos directos y {indirectos} amigos indirectos")
        print("La subred de amigos encontrada es la siguiente: ")
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
        for grado, amigo, lista, comun in lista_amigos:
            if comun:
                print(f"El usuario tiene una profundidad de: {grado}, id: {amigo}, y tiene la siguiente lista de hobbies: {lista} y tienen los siguientes hobbies con el usuario buscado: {comun}")
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
            else:
                print(f"El usuario tiene una profundidad de: {grado}, id: {amigo}, y tiene la siguiente lista de hobbies: {lista} pero no tienen ningun hobbie en comun con el usuario buscado")
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
    else:
        print("No se encontraron amigos con los mismos intereses")


def print_req_8(control):
    """
    Función que imprime la solución del Requerimiento 8 en consola.
    Permite graficar en un mapa los usuarios dentro de un radio dado desde unas coordenadas específicas.
    """
    center_lat = float(input("Ingrese la latitud del centro: "))
    center_lon = float(input("Ingrese la longitud del centro: "))
    radius_km = float(input("Ingrese el radio en kilómetros: "))
    
    resultado = logic.req_8(control, center_lat, center_lon, radius_km)
    
    mapa = resultado[0]
    tiempo = resultado[1]
    
    # Guardamos el mapa en un archivo HTML
    file_name = "usuarios_mapa.html"
    mapa.save(file_name)
    
    print(f'El tiempo del algoritmo fue {tiempo} ms')
    print(f"El mapa ha sido generado exitosamente y guardado como '{file_name}'.")
    print(f"Abra el archivo '{file_name}' en su navegador para visualizar el mapa interactivo.")
    #IMPORTANTE El archivo usuarios_mapa.html se guardará en el mismo directorio donde se está ejecutando el codigo de Python.



# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control, data_dir)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
