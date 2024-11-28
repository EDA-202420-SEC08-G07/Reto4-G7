from DataStructures.Tree import bst_node as bst_nd
from DataStructures.List import array_list as al
def new_map():
    """Crea una tabla de símbolos ordenada basada en un árbol binario de búsqueda (BST) vacía."""
    return {
        "root": None,
        "type": "BST"
    }   

def put(my_bst, key, value):
    """Inserta una pareja llave-valor en el BST. Si la llave ya existe, reemplaza el valor."""
    my_bst["root"]=insert_node(my_bst["root"], key, value)
    return my_bst

def insert_node(root, key, value):
    # Caso base -> Raíz = None, crea un nuevo nodo
    if root is None:
        return bst_nd.new_node(key, value)

    # Llave menor, inserta a la izquierda
    if key < root['key']:
        root['left'] = insert_node(root['left'], key, value)
    
    # Llave mayor, inserta a la derecha
    elif key > root['key']:
        root['right'] = insert_node(root['right'], key, value)
    
    # Llave igual, actualiza el valor
    else:
        root['value'] = value
    
    #actualizacion del tamanio
    root['size'] = 1 + node_size(root['left']) + node_size(root['right'])

    return root

def node_size(node):
    """Devuelve el tamaño del subárbol enraizado en `node`. Si es `None`, devuelve 0."""
    if node is None:
        return 0
    return node['size']

def get(my_bst, key):
    """
    Retorna la pareja lleve-valor con llave igual a key 
    Args:
        my_bst: El arbol de búsqueda 
        key: La llave asociada a la pareja
    """
    return get_node(my_bst['root'], key)

def get_node(root, key):
    if root is None:
        return None
    elif root['key'] == key:
        return root['value']
    elif key < root['key']:
        return get_node(root['left'], key)
    else: 
        return get_node(root['right'], key)
    
def remove(my_bst, key):
    my_bst['root'] = remove_node(my_bst['root'], key)
    
def remove_node(root, key):
    if root is None:
        return None  

    if key < root['key']:
        root['left'] = remove_node(root['left'], key)  
    elif key > root['key']:
        root['right'] = remove_node(root['right'], key)  
    else:
        # Caso 1: Nodo sin hijos (es una hoja)
        if root['left'] is None and root['right'] is None:
            return None  
        
        # Caso 2: Nodo con solo un hijo
        elif root['left'] is None:
            return root['right']  # Reemplazamos el nodo con su hijo derecho
        elif root['right'] is None:
            return root['left']  # Reemplazamos el nodo con su hijo izquierdo
        
        # Caso 3: Nodo con dos hijos
        else:
            # Buscamos el nodo sucesor (el menor del subárbol derecho)
            sucesor = min_key_nodo(root['right'])
            sucesor_value = min_key_nodo_value(root['right'])
            # Reemplazamos los datos del nodo actual con los del sucesor
            root['key'] = sucesor
            root['value'] = sucesor_value
            # Eliminamos el nodo sucesor del subárbol derecho
            root['right'] = delete_min_nodo(root['right'])
    
    # Actualizamos el tamaño del nodo
    root['size'] = 1 + node_size(root['left']) + node_size(root['right'])

    return root
    
def contains(my_bst, key):
    """
    Informa si la llave key se encuentra en la tabla de hash
    Args:
    my_bst: El arbol de búsqueda
    key: La llave a buscar
    Returns:
        True si la llave está presente False en caso contrario
    """
    return contains_nodo(my_bst['root'], key)

def contains_nodo(root, key):
    if root is None:
        return False
    if root['key'] == key:
        return True
    elif key < root['key']:
        return contains_nodo(root['left'], key)
    else: 
        return contains_nodo(root['right'], key)

def size(my_bst):
    """ 
    Retorna el número de entradas en la tabla de simbolos

    Args:
        my_bst (BST): El arbol de búsqueda
    Returns:
        El número de elementos en la tabla
    """
    if my_bst['root'] is None:
        return 0
    else:
        return my_bst['root']['size']

def is_empty(my_bst):
    """ 
    Informa si el mapa esta vacio

    Args:
        my_bst (BST): El mapa bst
    Returns:
        True si la tabla es vacía, False en caso contrario
    """
    contador = size(my_bst)
    if contador != 0:
        return False
    else:
        return True

def key_set(my_bst):
    """ 
    Retorna una lista con todas las llaves de la tabla

    Args:
        my_bst (BST): Bst con la info
    Returns:
        Una lista con todas las llaves de la tabla
    """
    key_list = al.new_list()  
    return key_set_tree(my_bst['root'], key_list)  

def key_set_tree(root, key_list):
    if root is not None:
        key_set_tree(root['left'], key_list)  
        al.add_last(key_list, root['key'])  
        key_set_tree(root['right'], key_list)  
    return key_list  

def value_set(my_bst):
    """ 
    Retorna una lista con todas los values de la tabla

    Args:
        my_bst (BST): Bst con la info
    Returns:
        Una lista con todas los valores de la tabla
    """
    value_list = al.new_list()  
    return value_set_tree(my_bst['root'], value_list)  

def value_set_tree(root, value_list):
    if root is not None:
        value_set_tree(root['left'], value_list)  
        al.add_last(value_list, root['value'])  
        value_set_tree(root['right'], value_list)  
    return value_list

def min_key(my_bst):
    """ 
    Retorna la menor llave de la tabla de simbolos

    Args:
        my_bst (BST): arbol de busqueda binaria
    Returns:
        Valor de la menor llave
    """
    if my_bst['root'] is None:
        return None
    else: 
        return min_key_nodo(my_bst['root'])
    
def min_key_nodo(root):
    if root['left'] is not None:
        return min_key_nodo(root['left'])
    else:
        return root['key']
def min_key_value(my_bst):
    if my_bst['root'] is None:
        return None
    else: 
        return min_key_nodo_value(my_bst['root'])
    
def min_key_nodo_value(root):
    if root['left'] is not None:
        return min_key_nodo(root['left'])
    else:
        return root['value']
    

def max_key(my_bst):
    """ 
    Retorna la menor llave de la tabla de simbolos

    Args:
        my_bst (BST): arbol de busqueda binaria
    Returns:
        Valor de la menor llave
    """
    if my_bst['root'] is None:
        return None
    else: 
        return max_key_nodo(my_bst['root'])
    
def max_key_nodo(root):
    if root['right'] is not None:
        return max_key_nodo(root['right'])
    else:
        return root['key']

def delete_min(my_bst):
    """ 
    Elimina el menor elemento del árbol de búsqueda binaria.

    Args:
        my_bst (BST): Árbol de búsqueda binaria.
        
    Returns:
        El árbol sin la llave más pequeña.
    """
    if my_bst['root'] is None:
        return my_bst  
    
    my_bst['root'] = delete_min_nodo(my_bst['root'])
    
    return my_bst

def delete_min_nodo(root):
    """
    Función recursiva que elimina el nodo con la menor clave en el subárbol.

    Args:
        root: Nodo raíz del subárbol.

    Returns:
        La nueva raíz del subárbol después de eliminar el nodo mínimo.
    """
    # Caso base: Si no hay un hijo izquierdo, este es el nodo mínimo
    if root['left'] is None:
        return root['right']  # Reemplaza el nodo actual con su hijo derecho (si lo tiene)
    
    root['left'] = delete_min_nodo(root['left'])

    root['size'] = 1 + node_size(root['left']) + node_size(root['right'])
    return root

def delete_max(my_bst):
    """ 
    Elimina el menor elemento del árbol de búsqueda binaria.

    Args:
        my_bst (BST): Árbol de búsqueda binaria.
        
    Returns:
        El árbol sin la llave más pequeña.
    """
    if my_bst['root'] is None:
        return my_bst  
    
    my_bst['root'] = delete_max_nodo(my_bst['root'])
    
    return my_bst

def delete_max_nodo(root):
    """
    Función recursiva que elimina el nodo con la menor clave en el subárbol.

    Args:
        root: Nodo raíz del subárbol.

    Returns:
        La nueva raíz del subárbol después de eliminar el nodo mínimo.
    """
    # Caso base: Si no hay un hijo derecho, este es el nodo mínimo
    if root['right'] is None:
        return root['left']  # Reemplaza el nodo actual con su hijo izquierdo (si lo tiene)
    
    root['right'] = delete_max_nodo(root['right'])

    root['size'] = 1 + node_size(root['left']) + node_size(root['right'])
    return root

def height(my_bst):
    """
    Retorna la altura del árbol de búsqueda binaria (BST).

    Args:
        my_bst: El árbol de búsqueda binaria (BST).

    Returns:
        int: La altura del árbol. Si el árbol está vacío, retorna -1.
    """
    if my_bst['root'] is None:
        return -1  # Si el árbol está vacío, la altura es -1
    
    return height_nodo(my_bst['root'])

def height_nodo(root):
    """
    Función auxiliar recursiva que calcula la altura de un subárbol.

    Args:
        root: Nodo raíz del subárbol.

    Returns:
        int: La altura del subárbol.
    """
    if root is None:
        return -1  # Caso base: Si el nodo es None, la altura es -1
    
    # Calculamos la altura de los subárboles izquierdo y derecho
    altura_izq = height_nodo(root['left'])
    altura_der = height_nodo(root['right'])
    
    # La altura del nodo actual es 1 más la altura máxima de sus hijos
    return 1 + max(altura_izq, altura_der)

def floor(my_bst, key):
    """ 
    Retorna la llave más grande en la tabla de símbolos que es menor o igual a la llave dada.

    Args:
        my_bst (BST): El árbol de búsqueda binaria.
        key (int): La llave de búsqueda.

    Returns:
        La llave más grande menor o igual a key, o None si no existe.
    """
    return floor_node(my_bst['root'], key)

def floor_node(root, key):
    if root is None:
        return None  
    if root['key'] == key:
        return root['key']
    if key < root['key']:
        return floor_node(root['left'], key)  
    if key > root['key']:
        pizza = floor_node(root['right'], key)
        if pizza is not None:
            return pizza
        else:
            return root['key']  
        
def ceiling(my_bst, key):
    """ 
    Retorna la llave más pequeña en la tabla de símbolos que es mayor o igual a la llave dada.

    Args:
        my_bst (BST): El árbol de búsqueda binaria.
        key (int): La llave de búsqueda.

    Returns:
        La llave más pequeña mayor o igual a key, o None si no existe.
    """
    return ceiling_node(my_bst['root'], key)

def ceiling_node(root, key):
    if root is None:
        return None 
    if root['key'] == key:
        return root['key']
    if key > root['key']:
        return ceiling_node(root['right'], key)  
    if key < root['key']:
        papu = ceiling_node(root['left'], key)
        if papu is not None:
            return papu 
        else:
            return root['key'] 

def select(my_bst, pos):
    """ 
    Retorna la k-ésima llave más pequeña del árbol de búsqueda.

    Args:
        my_bst (BST): Árbol de búsqueda binaria.
        pos (int): Posición de la k-ésima llave más pequeña (0-indexed).

    Returns:
        La llave correspondiente a la posición `pos` o None si no existe.
    """
    return select_node(my_bst['root'], pos)

def select_node(root, pos):
    if root is None:
        return None  
    
    # Tamaño del subárbol izquierdo
    izq_tam = node_size(root['left']) if root['left'] else 0
    if izq_tam == pos:
        return root['key']
    elif pos < izq_tam:
        return select_node(root['left'], pos)
    else:
        return select_node(root['right'], pos - izq_tam - 1)

def rank(my_bst, key):
    """ 
    Retorna el número de llaves estrictamente menores que `key` en el árbol de búsqueda binaria.

    Args:
        my_bst (BST): Árbol de búsqueda binaria.
        key (int): La llave de búsqueda.

    Returns:
        El número de llaves estrictamente menores que `key`.
    """
    return rank_node(my_bst['root'], key)

def rank_node(root, key):
    if root is None:
        return 0  
    if key < root['key']:
        return rank_node(root['left'], key)
    # Si la llave buscada es mayor que la llave en el nodo actual, sumamos el tamaño del subárbol izquierdo
    # (todas las llaves en el subárbol izquierdo son menores) + 1 por la llave actual, y buscamos en el subárbol derecho
    elif key > root['key']:
        left_size = node_size(root['left']) if root['left'] else 0
        return 1 + left_size + rank_node(root['right'], key)
    # Si la llave buscada es igual a la llave en el nodo actual, el número de llaves menores es el tamaño del subárbol izquierdo
    else:
        return node_size(root['left']) if root['left'] else 0
    
def keys(my_bst, key_lo, key_hi):
    """ 
    Retorna todas las llaves del árbol que se encuentren en el rango [key_lo, key_hi].
    
    Args:
        my_bst (BST): El árbol de búsqueda binaria.
        key_lo (int): Límite inferior del rango.
        key_hi (int): Límite superior del rango.
    
    Returns:
        Una lista con las llaves en el rango especificado.
    """
    if my_bst is None:
        return my_bst
    else: 
        key_list = al.new_list()
        return keys_in_range(my_bst['root'], key_lo, key_hi, key_list)

def keys_in_range(root, key_lo, key_hi, key_list):
    """ 
    Función recursiva que encuentra todas las llaves en el rango [key_lo, key_hi] en el árbol de búsqueda binaria.
    
    Args:
        root: El nodo raíz del subárbol.
        key_lo (int): Límite inferior del rango.
        key_hi (int): Límite superior del rango.
        key_list (list): Lista donde se almacenan las llaves en el rango.
    
    Returns:
        key_list (list): Lista con las llaves en el rango [key_lo, key_hi].
    """
    if root is None:
        return key_list  # Si el nodo es None, no hay más llaves que agregar
    # Si la llave actual es mayor que el límite inferior, revisamos el subárbol izquierdo
    if key_lo < root['key']:
        keys_in_range(root['left'], key_lo, key_hi, key_list)
    # Si la llave actual está dentro del rango, la agregamos a la lista
    if key_lo <= root['key'] <= key_hi:
        al.add_last(key_list, root['key'])
    # Si la llave actual es menor que el límite superior, revisamos el subárbol derecho
    if root['key'] < key_hi:
        keys_in_range(root['right'], key_lo, key_hi, key_list)
    
    return key_list

def values(my_bst, key_lo, key_hi):
    """ 
    Retorna todas los values del árbol que se encuentren en el rango [key_lo, key_hi].
    
    Args:
        my_bst (BST): El árbol de búsqueda binaria.
        key_lo (int): Límite inferior del rango.
        key_hi (int): Límite superior del rango.
    
    Returns:
        Una lista con los valores en el rango especificado.
    """
    if my_bst is None:
        return my_bst
    else: 
        value_list = al.new_list()
        return values_in_range(my_bst['root'], key_lo, key_hi, value_list)

def values_in_range(root, key_lo, key_hi, value_list):
    if root is None:
        return value_list 
    # Si la llave actual es mayor que el límite inferior, revisamos el subárbol izquierdo
    if key_lo < root['key']:
        values_in_range(root['left'], key_lo, key_hi, value_list)
    # Si la llave actual está dentro del rango, la agregamos a la lista
    if key_lo <= root['key'] <= key_hi:
        al.add_last(value_list, root['value'])
    # Si la llave actual es menor que el límite superior, revisamos el subárbol derecho
    if root['key'] < key_hi:
        values_in_range(root['right'], key_lo, key_hi, value_list)
    return value_list

