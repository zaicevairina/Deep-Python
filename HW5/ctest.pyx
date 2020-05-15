cpdef test(list  matrix_1, list matrix_2, tuple size_1, tuple size_2):
    cdef list result = []
    cdef int a = 0
    cdef int b = 0
    cdef int c = 0
    cdef list res
    cdef int j = 0
    cdef int el = 0
    cdef int m = 0
    cdef int k = 0
    if size_1[1] != size_2[0]:
            return 'Нельзя перемножить матрицы таких размерностей'
    else:
        a = (size_1[1])
        b = (size_1[0])
        c = (size_2[1])
        for i in range(b):
            res = []
            j = 0
            for j in range(c):
                el = 0
                m = 0
                k = 0
                for k in range(a):
                    m = matrix_1[i][k] * matrix_2[k][j]
                    el += m
                res.append(el)
            result.append(res)
        return (result)