from copy import deepcopy
import ctest


class Matrix:
    def __init__(self, list_of_lists):
        self.matrix = deepcopy(list_of_lists)

    def __str__(self):
        return '\n'.join('\t'.join(map(str, row))
                         for row in self.matrix)

    def size(self):
        sizepair = (len(self.matrix), len(self.matrix[0]))
        return sizepair

    def __getitem__(self, idx):
        return self.matrix[idx[0]][idx[1]]

    def __add__(self, other):

        result = []
        numbers = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                summa = other.matrix[i][j] + self.matrix[i][j]
                numbers.append(summa)
                if len(numbers) == len(self.matrix):
                    result.append(numbers)
                    numbers = []
        return Matrix(result)

    def __mul__(self, other):
        if isinstance(other, int):
            result = [[other * x for x in y] for y in self.matrix]
            return Matrix(result)
        elif self.size()[1] != other.size()[0]:
            return 'Нельзя перемножить матрицы таких размерностей'
        else:
            a = range(self.size()[1])
            b = range(self.size()[0])
            c = range(other.size()[1])
            result = []
            for i in b:
                res = []
                for j in c:
                    el, m = 0, 0
                    for k in a:
                        m = self.matrix[i][k] * other.matrix[k][j]
                        el += m
                    res.append(el)
                result.append(res)
            return Matrix(result)

    def cmul(self, other):
        if isinstance(other, Matrix):
            return ctest.test(self.matrix, other.matrix, self.size(), other.size())

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            result = [[x / other for x in y] for y in self.matrix]
            return Matrix(result)

    def T(self):
        a = range(self.size()[0])
        b = range(self.size()[1])
        result = [[0 for _ in (a)] for _ in (b)]
        for i in a:
            for j in b:
                result[j][i] = self[(i, j)]

        return Matrix(result)

    def __contains__(self, number):
        if (isinstance(number, int)):
            for row in self.matrix:
                if number in row:
                    return True
        return False

    def __eq__(self, other):
        return self.matrix == other.matrix


import time

if __name__ == "__main__":
    a = [[1, 2, 7, 4], [3, 4, 6, 4], [3, 6, 9, 6], [4, 5, 6, 7]]
    matrix = Matrix(a)
    start = time.clock()
    res1 = matrix * matrix
    end = time.clock()
    print("Python time = {:.10f}".format(end - start))
    python = end - start
    start = time.clock()
    res2 = (matrix.cmul(matrix))
    end = time.clock()
    print("Cython time = {:.10f}".format(end - start))
    print(f"Cython быстрее Python в {python / (end - start)} раз")

    assert ((1 in Matrix([[1, 2], [3, 4]])) == True)
    assert ((Matrix([[1, 2], [3, 4]]))[1, 1] == 4)
    assert (Matrix([[1, 2], [3, 4]]) + Matrix([[0, 1], [1, 0]])) == Matrix([[1, 3], [4, 4]])
    assert (Matrix([[1, 2], [3, 4]]) * 5 == Matrix([[5, 10], [15, 20]]))
    assert (Matrix([[2, 4], [6, 8]]) / 2 == Matrix([[1, 2], [3, 4]]))
    assert (Matrix([[1, 2], [3, 4]]) * Matrix([[0, 1], [1, 0]])) == Matrix([[2, 1], [4, 3]])
    assert (Matrix([[1, 2], [3, 4]]).T() == Matrix([[1, 3], [2, 4]]))
    assert (Matrix([[1, 1,1], [2,2, 2]]).T() == Matrix([[1, 2],[1,2], [1, 2]]))

    assert (res1 == Matrix(res2))