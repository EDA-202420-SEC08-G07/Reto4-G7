from . import map_entry as me
from . import map_functions as mf
import random as rd
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sl


def new_map(num_elements, load_factor, prime=109345121):
    """
    crea un nuevo mapa (sin elementos)
    Atributos:
    - Prime : Numero primo utilizado en la funcion de Hash
    - Capacity: Tamanio de la tabla. Siguiente num_prime superior a "num_elements / load_factor"
    - Scale: Numero aleatorio entre 1 y prime - 1
    - Shift: Numero aleatorio entre 0 y prime - 1 
    - Table: Lista de tamanio 'Capacity' con las entradas de la tabla
    - Current_factor: Factor de carga actual de la tabla. Inicializado en 0
    - Limit_factor: Factor de carga maximo de la tabla (load_factor)
    - Size: Tamanio de la lista
    - Type: PROBING

    Args:
        num_elements (_type_): Numero de elementos <llave-valor> (int)
        load_factor (_type_): Factor de carga maximo de la tabla (float)
        prime (int, optional): Numero primo utilizado en la funcion de Hash. Defaults to 109345121.
        
    Return:
        Un nuevo map (map_separate_probing)
    """
    capacity = mf.next_prime(num_elements//load_factor)
    scale = rd.randint(1, prime-1) 
    shift = rd.randint(0, prime-1)
    hashtable = {'prime': prime,
                'capacity': capacity,
                'scale': scale,
                'shift': shift,
                'table': None,
                'current_factor': 0,
                'limit_factor':load_factor,
                'size': 0,
                'type': 'PROBING'
    }
    hashtable['table'] = lt.new_list() 
    for _ in range(capacity):
        entry = me.new_map_entry(None, None)
        lt.add_last(hashtable['table'], entry)
        
    return hashtable

def put(my_map, key, value):
    """
    Ingresa una pareja llave, valor a la tabla de hash. Si la llave ya existe en la tabla, se reemplaza el valor.

    Parameters:
    my_map (map_linear_probing) – El map a donde se guarda la pareja llave-valor

    key (any) – la llave asociada a la pareja

    value (any) – el valor asociado a la pareja

    Returns:
    El map
    Return type:
    map_linear_probing
    """
    # Calcular el hash de la llave
    valor = mf.hash_value(my_map, key)

    # Verificar si es necesario expandir la capacidad
    if my_map['capacity'] < mf.next_prime((my_map['size'] + 1) // my_map['limit_factor']):
        capacidad = my_map['capacity']
        n = capacidad * 2
        new_capacity = mf.next_prime(n)
        my_map['capacity'] = new_capacity
        # Realizar el rehashing de los elementos existentes
        rehash(my_map)

    # Implementar Linear Probing
    for i in range(my_map['capacity']):
        index = (valor + i) % my_map['capacity']
        if index <= my_map['capacity']:
            if my_map['table']['elements'][index]['key'] is None or my_map['table']['elements'][index]['value'] == '__EMPTY__':
                my_map['table']['elements'][index]['value'] = value
                my_map['table']['elements'][index]['key'] = key
                my_map['size'] += 1
                return my_map
        if index > my_map['capacity']:
            for j in range(my_map['capacity']):
                if j == index:
                    return my_map
                else:
                    if my_map['table']['elements'][j]['key'] is None or my_map['table']['elements'][j]['value'] == '__EMPTY__':
                        my_map['table']['elements'][j]['value'] = value
                        my_map['table']['elements'][j]['key'] = key
                        my_map['size'] += 1
                        return my_map
    return my_map 

def rehash(my_map):
    """
    Rehashear los elementos existentes en el mapa después de una expansión de capacidad.
    """
    old_table = my_map['table']['elements']
    new_capacity = my_map['capacity']
    my_map['table']['elements'] = [{'key': None, 'value': '__EMPTY__'} for _ in range(new_capacity)]
    my_map['size'] = 0  # Reiniciamos el tamaño para recalcular al insertar de nuevo los elementos

    for element in old_table:
        if element['key'] is not None and element['value'] != '__EMPTY__':
            put(my_map, element['key'], element['value'])  # Reinsertamos cada elemento en la nueva tabla


def contains(my_map, key):
    """
    Valida si la llave key se encuentra en el map

    Retorna True si la llave key se encuentra en el my_map o False en caso contrario.

    Parameters:
    my_map (map_linear_probing) – El my_map a donde se guarda la pareja

    key (any) – la llave asociada a la pareja

    Returns:
    True si la llave se encuentra en el map, False en caso contrario

    Return type: bool
    """
    valor = mf.hash_value(my_map, key)

    for i in range(my_map['capacity']):
        index = (valor + i) % my_map['capacity']  # Linear probing
        element = my_map['table']['elements'][index]
        
        # Si encontramos una celda vacía o marcada como '__EMPTY__', no existe la llave
        if element['key'] is None:
            return False
        if element['key'] == key:
            return True
    
    return False

def contains_mas_indice(my_map, key):
    """
    Valida si la llave key se encuentra en el map

    Retorna True si la llave key se encuentra en el my_map o False en caso contrario, y el índice.

    Parameters:
    my_map (map_linear_probing) – El my_map a donde se guarda la pareja

    key (any) – la llave asociada a la pareja

    Returns:
    True si la llave se encuentra en el map, False en caso contrario, e índice de la llave si existe.

    Return type: (bool, int)
    """
    valor = mf.hash_value(my_map, key)

    for i in range(my_map['capacity']):
        index = (valor + i) % my_map['capacity']  # Linear probing
        element = my_map['table']['elements'][index]
        
        # Si encontramos una celda vacía o marcada como '__EMPTY__', no existe la llave
        if element['key'] is None:
            return False, None
        if element['key'] == key:
            return True, index
    
    return False, None

        
def get(my_map, key):
    """
    Retorna el valor asociado a la llave key en el map

    Parametros:
        my_map (map_linear_probing) – El my_map a donde se guarda la pareja
        key (any) – la llave asociada a la pareja
    Return: Valor asociado a la llave key (any)
    """
    calificador, index = contains_mas_indice(my_map, key)
    if calificador:
        return my_map['table']['elements'][index]['value']

def remove(my_map, key):
    """ 
    Elimina la pareja llave-valor del map

    Args:
        my_map (map_linear_probing) – El map a examina
        key (any) – Llave a eliminar
    Return: El map sin la llave key
    """
    calificador, index = contains_mas_indice(my_map, key)
    if calificador:
        my_map['table']['elements'][index]['key'] = '__EMPTY__'
        my_map['table']['elements'][index]['value'] = '__EMPTY__'
        my_map['size'] -= 1
    return my_map



def size(my_map):
    """
    Retorna el número de parejas llave-valor en el map

    Parameters
    :
    my_map (map_linear_probing) – El map a examinar

    Returns
    :
    Número de parejas llave-valor en el map

    Return type
    :
    int
    """
    return my_map['size']

def is_empty(my_map):
    """
    Indica si el map se encuentra vacío

    Parameters: my_map (map_linear_probing) – El map a examinar
    return: True si el map está vacío, False en caso contrario (bool)
    """
    return my_map['size'] == 0

def key_set(my_map):
    """
    Retorna una lista con todas las llaves de la tabla de hash

    Args:
        my_map (map_linear_probing) – El map a examinar
    returns:
        lista de llaves (array_list)
    """
    lst = []
    contador = 0
    for i in range(my_map['capacity']):
        if my_map['table']['elements'][i]['key'] != None and my_map['table']['elements'][i]['key'] != '__EMPTY__' :
            lst.append(my_map['table']['elements'][i]['key'])
            contador += 1
    array_lst = {'elements': lst, 'size': contador}
    return array_lst

def value_set(my_map):
    """
    Retorna una lista con todas los values de la tabla de hash

    Args:
        my_map (map_linear_probing) – El map a examinar
    returns:
        lista de values (array_list)
    """
    lst = []
    contador = 0
    for i in range(my_map['capacity']):
        if my_map['table']['elements'][i]['key'] != None and my_map['table']['elements'][i]['key'] != '__EMPTY__' :
            lst.append(my_map['table']['elements'][i]['value'])
            contador += 1
    array_lst = {'elements': lst, 'size': contador}
    return array_lst

def find_slot(my_map, key, hash_value):
    """
    Busca la key a partir de una posición dada en la tabla.

    Utiliza la función de hash para encontrar la posición inicial de la llave.
    Si la posición está ocupada, busca la siguiente posición disponible.

    Args:
        my_map (map_linear_probing) – El map a examinar
        key (any) – Llave a buscar
        hash_value (int) – Posición inicial de la llave
    Returns:
        Retorna una tupla con dos valores. El primero indica si la posición está ocupada, 
        True si se encuentra la key de lo contrario False. El segundo la posición en la tabla de hash 
        donde se encuentra o posición libre para agregarla (bool, int)
    """
    ya_esta, valor = contains_mas_indice(my_map, key)
    if ya_esta and valor == hash_value:
        return True, valor

    for i in range(my_map['capacity']):
        index = (hash_value + i) % my_map['capacity']  
        element = my_map['table']['elements'][index]
        if element['key'] is None or element['value'] == '__EMPTY__':
            return False, index
    return False, -1

def is_available(table, pos):
    """
    Informa si la posición pos está disponible en la tabla de hash.
    Se entiende que una posición está disponible si su contenido es igual a None (no se ha usado esa posición) o a __EMPTY__ (la posición fue liberada)

    Args:
        table (array_list) – Tabla de hash, implementada como una lista (array_list)
        pos (int) – Posición a verificar
    Returns: 
        True si la posición está disponible, False en caso contrario
    """
    skikiby_toilet = False
    if table['elements'][pos]['key'] == None or table['elements'][pos]['key'] == '__EMPTY__' :
        skikiby_toilet = True
    return skikiby_toilet

def rehash(my_map):
    """
    Hace rehash de todos los elementos de la tabla de hash.

    Incrementa la capacidad de la tabla al doble, y la acerca al primo mayor mas cercano
    y se hace rehash de todos los elementos de la tabla uno por uno.

    Se utiliza la función hash_value para calcular el nuevo hash de cada llave.

    Args:
        my_map (map_linear_probing) – El map a hacer rehash
    Returns:
        El map con la nueva capacidad
    """
    capacidad = my_map['capacity']
    n = capacidad * 2
    new_capacity = mf.next_prime(n)
    my_map['capacity'] = new_capacity
    tabla_ant = my_map['table']
    my_map['table'] = {'elements': [{'key': None, 'value': None} for w in range(new_capacity)]}
    for element in tabla_ant['elements']:
        if element['key'] is not None and element['value'] != '__EMPTY__':
            new_hash = mf.hash_value(my_map, element['key'])
            w, new_index = find_slot(my_map, element['key'], new_hash)
            my_map['table']['elements'][new_index] = {
                'key': element['key'],
                'value': element['value']
            }
    return my_map