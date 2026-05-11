def intercalacion_pasos(a, b):
    pasos, resultado = [], []
    i = j = 0
    a_sort, b_sort = sorted(a), sorted(b)
    while i < len(a_sort) and j < len(b_sort):
        pasos.append(("cmp", list(resultado), i, j))
        if a_sort[i] <= b_sort[j]:
            resultado.append(a_sort[i]); i += 1
        else:
            resultado.append(b_sort[j]); j += 1
        pasos.append(("add", list(resultado), i, j))
    while i < len(a_sort):
        resultado.append(a_sort[i]); i += 1
        pasos.append(("add", list(resultado), i, j))
    while j < len(b_sort):
        resultado.append(b_sort[j]); j += 1
        pasos.append(("add", list(resultado), i, j))
    return resultado, pasos

def mezcla_directa_pasos(lista):
    pasos = []
    def merge_sort(a):
        if len(a) <= 1: return a
        m = len(a) // 2
        L, R = merge_sort(a[:m]), merge_sort(a[m:])
        return merge(L, R)
    def merge(L, R):
        res, i, j = [], 0, 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: res.append(L[i]); i += 1
            else: res.append(R[j]); j += 1
            pasos.append(list(res) + L[i:] + R[j:])
        res += L[i:] + R[j:]
        pasos.append(list(res))
        return res
    resultado = merge_sort(list(lista))
    return resultado, pasos

def mezcla_equilibrada_pasos(lista, k=3):
    pasos = []
    sublistas = [[] for _ in range(k)]
    for idx, el in enumerate(lista): sublistas[idx % k].append(el)
    sublistas = [sorted(s) for s in sublistas if s]
    pasos.append(("split", [item for s in sublistas for item in s]))
    def merge2(a, b):
        res, i, j = [], 0, 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]: res.append(a[i]); i += 1
            else: res.append(b[j]); j += 1
        return res + a[i:] + b[j:]
    while len(sublistas) > 1:
        nueva = []
        for i in range(0, len(sublistas), 2):
            if i + 1 < len(sublistas): nueva.append(merge2(sublistas[i], sublistas[i+1]))
            else: nueva.append(sublistas[i])
        sublistas = nueva
        pasos.append(("merge", sublistas[0] if len(sublistas) == 1 else [x for s in sublistas for x in s]))
    return sublistas[0], pasos