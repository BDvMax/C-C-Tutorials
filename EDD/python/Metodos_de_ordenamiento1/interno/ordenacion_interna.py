def burbuja(arr):
    arr = arr[:]
    pasos = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                pasos.append(arr[:])
    return arr, pasos

def insercion(arr):
    arr = arr[:]
    pasos = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            pasos.append(arr[:])
        arr[j + 1] = key
        pasos.append(arr[:])
    return arr, pasos

def seleccion(arr):
    arr = arr[:]
    pasos = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            pasos.append(arr[:])
    return arr, pasos

def shell_sort(arr):
    arr = arr[:]
    n = len(arr)
    gap = n // 2
    pasos = []
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                pasos.append(arr[:])
            arr[j] = temp
            pasos.append(arr[:])
        gap //= 2
    return arr, pasos

def quick_sort_steps(arr, pasos, inicio, fin):
    if inicio < fin:
        pivot = arr[fin]
        i = inicio - 1
        for j in range(inicio, fin):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                pasos.append(arr[:])
        arr[i + 1], arr[fin] = arr[fin], arr[i + 1]
        pasos.append(arr[:])
        pi = i + 1
        quick_sort_steps(arr, pasos, inicio, pi - 1)
        quick_sort_steps(arr, pasos, pi + 1, fin)

def quick_sort(arr):
    arr = arr[:]
    pasos = []
    quick_sort_steps(arr, pasos, 0, len(arr) - 1)
    return arr, pasos

def heapify(arr, n, i, pasos):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        pasos.append(arr[:])
        heapify(arr, n, largest, pasos)

def heap_sort(arr):
    arr = arr[:]
    n = len(arr)
    pasos = []
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, pasos)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        pasos.append(arr[:])
        heapify(arr, i, 0, pasos)
    return arr, pasos

def counting_sort_by_digit(arr, exp, pasos):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    for i in range(n):
        arr[i] = output[i]
    pasos.append(arr[:])

def radix_sort(arr):
    arr = arr[:]
    pasos = []
    if not arr: return arr, pasos
    
    # Manejo básico para evitar errores si hay strings o negativos
    try:
        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            counting_sort_by_digit(arr, exp, pasos)
            exp *= 10
    except TypeError:
        pass # Radix sort numérico omitido si hay strings
    return arr, pasos