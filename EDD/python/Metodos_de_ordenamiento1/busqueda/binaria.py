"""
Librería personalizada para algoritmos de Búsqueda Binaria.
Nota: Recuerda que para que la búsqueda binaria funcione, 
la lista DEBE estar ordenada previamente.
"""

def busqueda_binaria_iterativa(lista, objetivo):
    """
    Busca un elemento en una lista ordenada de forma iterativa.
    
    Argumentos:
    lista -- Lista de elementos ordenados.
    objetivo -- El elemento que se desea buscar.
    
    Retorna:
    El índice del elemento si se encuentra, de lo contrario -1.
    """
    izquierda = 0
    derecha = len(lista) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        
        # Elemento encontrado
        if lista[medio] == objetivo:
            return medio
        # Si el objetivo es mayor, ignoramos la mitad izquierda
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        # Si el objetivo es menor, ignoramos la mitad derecha
        else:
            derecha = medio - 1
            
    return -1


def busqueda_binaria_recursiva(lista, objetivo, izquierda=0, derecha=None):
    """
    Busca un elemento en una lista ordenada de forma recursiva.
    """
    if derecha is None:
        derecha = len(lista) - 1

    # Caso base: el elemento no está en la lista
    if izquierda > derecha:
        return -1

    medio = (izquierda + derecha) // 2

    # Elemento encontrado
    if lista[medio] == objetivo:
        return medio
    # Buscar en la mitad derecha
    elif lista[medio] < objetivo:
        return busqueda_binaria_recursiva(lista, objetivo, medio + 1, derecha)
    # Buscar en la mitad izquierda
    else:
        return busqueda_binaria_recursiva(lista, objetivo, izquierda, medio - 1)


def buscar_primer_limite(lista, objetivo):
    """
    Busca la PRIMERA aparición de un elemento (útil si hay duplicados).
    """
    izquierda, derecha = 0, len(lista) - 1
    resultado = -1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == objetivo:
            resultado = medio
            derecha = medio - 1  # Seguimos buscando a la izquierda
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
            
    return resultado


def buscar_ultimo_limite(lista, objetivo):
    """
    Busca la ÚLTIMA aparición de un elemento (útil si hay duplicados).
    """
    izquierda, derecha = 0, len(lista) - 1
    resultado = -1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == objetivo:
            resultado = medio
            izquierda = medio + 1  # Seguimos buscando a la derecha
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
            
    return resultado