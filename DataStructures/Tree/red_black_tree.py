from . import rbt_node as rbn
from DataStructures.List import array_list as al

RED = 0
BLACK = 1

def new_map():
    """Crea una tabla de símbolos ordenada basada en un árbol binario de búsqueda (BST) vacía."""
    return {
        "root": None,
        "type": "RBT"
    }   

def rotate_left(nodo):
    """Función que rota a la izquierda"""
    derecho = nodo['right']
    nodo['right'] = derecho['left']  
    derecho['left'] = nodo
    derecho['color'] = nodo['color']
    nodo['color'] = RED
    nodo["size"] = 1 + nodo_size(nodo["left"]) + nodo_size(nodo["right"])
    derecho["size"] = 1 + nodo_size(derecho["left"]) + nodo_size(derecho["right"])
    return derecho

def rotate_right(nodo):
    """Rotación a la derecha alrededor de un nodo."""
    izquierdo = nodo["left"]
    nodo["left"] = izquierdo["right"]  
    izquierdo["right"] = nodo
    izquierdo["color"] = nodo["color"]
    nodo["color"] = RED
    nodo["size"] = 1 + nodo_size(nodo["left"]) + nodo_size(nodo["right"])
    izquierdo["size"] = 1 + nodo_size(izquierdo["left"]) + nodo_size(izquierdo["right"])
    return izquierdo  

def flip_node_color(my_node):
    """
    Cambia el color de un nodo entre rojo y negro
    Args:
        my_node: El nodo cuyo color cambiar
    Returns:
        None
    Raises:
        Exception
    """
    my_node["color"] = BLACK if my_node["color"] == RED else RED


def flip_colors(my_node):
    """
    Cambia los colores del nodo y de sus dos hijos
    Args:
        my_node: El nodo cuyo color cambiar junto con sus hijos
    Returns:
        None
    Raises:
        Exception
    """
    flip_node_color(my_node)
    if my_node["left"] is not None:
        flip_node_color(my_node["left"])
    if my_node["right"] is not None:
        flip_node_color(my_node["right"])
        
def put(my_rbt, key, value):
    """Inserta una pareja llave-valor en el RBT. Si la llave ya existe, reemplaza el valor."""
    my_rbt['root'] = insert_node(my_rbt['root'], key, value)
    my_rbt['root']['color'] = BLACK
    return my_rbt

def insert_node(root, key, value):
    """
    Inserta una nueva pareja <llave, valor> en el árbol rojo-negro y equilibra el árbol.
    Args:
        my_rbt: El nodo raíz actual del árbol
        key: La llave del nuevo nodo
        value: El valor del nuevo nodo
    Returns:
        El nodo raíz del árbol ajustado
    """
    if root is None:
        # Caso base: crear un nuevo nodo rojo con la clave y el valor
        return rbn.new_node(key, value)
    
    if key < root["key"]:
        root["left"] = insert_node(root["left"], key, value)
    elif key > root["key"]:
        root["right"] = insert_node(root["right"], key, value)
    else:
        # Si la clave ya existe, actualizamos el valor
        root["value"] = value

    # Ajustes para mantener las propiedades del árbol rojo-negro

    # Si el hijo derecho es rojo y el izquierdo no, rotar a la izquierda
    if root["right"] is not None and rbn.is_red(root["right"]) and not (root["left"] is not None and rbn.is_red(root["left"])):
        root = rotate_left(root)

    # Si el hijo izquierdo es rojo y su hijo izquierdo también, rotar a la derecha
    if root["left"] is not None and rbn.is_red(root["left"]) and root["left"]["left"] is not None and rbn.is_red(root["left"]["left"]):
        root = rotate_right(root)

    # Si ambos hijos son rojos, invertir los colores
    if root["left"] is not None and root["right"] is not None and rbn.is_red(root["left"]) and rbn.is_red(root["right"]):
        flip_colors(root)
    root['size'] = 1 + nodo_size(root['left']) + nodo_size(root['right'])
    
    return root


def nodo_size(my_node):
    """
    Devuelve el tamaño del subárbol que cuelga del nodo dado.
    Si el nodo es None, devuelve 0.
    """
    if my_node is None:
        return 0
    return my_node["size"]

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

    root['size'] = 1 + nodo_size(root['left']) + nodo_size(root['right'])
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

    root['size'] = 1 + nodo_size(root['left']) + nodo_size(root['right'])
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
        return -1 
    
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
        return -1  
    
    altura_izq = height_nodo(root['left'])
    altura_der = height_nodo(root['right'])
    
    return 1 + max(altura_izq, altura_der)

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
        return key_list  
    if key_lo < root['key']:
        keys_in_range(root['left'], key_lo, key_hi, key_list)
    if key_lo <= root['key'] <= key_hi:
        al.add_last(key_list, root['key'])
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
    if key_lo < root['key']:
        values_in_range(root['left'], key_lo, key_hi, value_list)
    if key_lo <= root['key'] <= key_hi:
        al.add_last(value_list, root['value'])
    if root['key'] < key_hi:
        values_in_range(root['right'], key_lo, key_hi, value_list)
    return value_list




