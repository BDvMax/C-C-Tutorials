"""
Métodos de Ordenamiento en Python
==================================
Implementación de: ShellSort, QuickSort, HeapSort y Radix Sort
"""

# ─────────────────────────────────────────────
#  1. SHELL SORT
# ─────────────────────────────────────────────
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


# ─────────────────────────────────────────────
#  2. QUICK SORT
# ─────────────────────────────────────────────
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


# ─────────────────────────────────────────────
#  3. HEAP SORT
# ─────────────────────────────────────────────
def heapify(arr, n, i):
    largest = i
    left  = 2 * i + 1
    right = 2 * i + 2
    if left  < n and arr[left]  > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


# ─────────────────────────────────────────────
#  4. RADIX SORT
# ─────────────────────────────────────────────
def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count  = [0] * 10
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

def radix_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    return arr


# ─────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ─────────────────────────────────────────────
def leer_numeros():
    while True:
        try:
            cantidad = int(input("\n¿Cuántos números deseas ingresar? "))
            if cantidad < 1:
                print("  ⚠  Ingresa al menos 1 número.")
                continue
            break
        except ValueError:
            print("  ⚠  Por favor ingresa un número entero válido.")

    numeros = []
    print(f"Ingresa {cantidad} número(s) entero(s):")
    for i in range(cantidad):
        while True:
            try:
                num = int(input(f"  Número {i + 1}: "))
                numeros.append(num)
                break
            except ValueError:
                print("  ⚠  Ingresa un número entero válido.")
    return numeros

def mostrar_menu():
    print("\n" + "=" * 45)
    print("   MENÚ DE MÉTODOS DE ORDENAMIENTO")
    print("=" * 45)
    print("  1. Shell Sort")
    print("  2. Quick Sort")
    print("  3. Heap Sort")
    print("  4. Radix Sort")
    print("  5. Salir")
    print("=" * 45)

def main():
    print("\n╔══════════════════════════════════════════╗")
    print("║   PROGRAMA DE ORDENAMIENTO EN PYTHON     ║")
    print("╚══════════════════════════════════════════╝")

    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-5): ").strip()

        if opcion == "5":
            print("\n¡Hasta luego! 👋\n")
            break

        if opcion not in ("1", "2", "3", "4"):
            print("  ⚠  Opción inválida. Elige entre 1 y 5.")
            continue

        numeros = leer_numeros()
        print(f"\nLista original : {numeros}")

        if opcion == "1":
            resultado = shell_sort(numeros[:])
            metodo = "Shell Sort"
        elif opcion == "2":
            resultado = quick_sort(numeros[:])
            metodo = "Quick Sort"
        elif opcion == "3":
            resultado = heap_sort(numeros[:])
            metodo = "Heap Sort"
        else:  # opcion == "4"
            if any(n < 0 for n in numeros):
                print("  ⚠  Radix Sort solo admite números no negativos.")
                continue
            resultado = radix_sort(numeros[:])
            metodo = "Radix Sort"

        print(f"Lista ordenada ({metodo}): {resultado}")

if __name__ == "__main__":
    main()