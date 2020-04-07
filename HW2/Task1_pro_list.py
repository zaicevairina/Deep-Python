class list_pro(list):

    def __init__(self, *args):
        super().__init__(args)

    def __add__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sub = len(self) - len(other)
            if sub == 0:
                return list_pro(*[i + j for i, j in zip(self, other)])
            elif sub > 0:
                x = other[::]
                x.extend([0] * sub)
                return list_pro(*[i + j for i, j in zip(self, x)])
            else:
                x = self[::]
                x.extend([0] * (-sub))
                return list_pro(*[i + j for i, j in zip(x, other)])
        else:
            raise ValueError

    def __sub__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sub = len(self) - len(other)
            if sub == 0:
                return list_pro(*[i - j for i, j in zip(self, other)])
            elif sub > 0:
                x = other[::]
                x.extend([0] * sub)
                return list_pro(*[i - j for i, j in zip(self, x)])
            else:
                x = self[::]
                x.extend([0] * (-sub))
                return list_pro(*[i - j for i, j in zip(x, other)])
        else:
            raise ValueError

    def __lt__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sum_other = sum(other)
            sum_self = sum(self)
            return True if sum_self < sum_other else False

        else:
            raise ValueError

    def __le__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sum_other = sum(other)
            sum_self = sum(self)
            return True if sum_self <= sum_other else False

        else:
            raise ValueError

    def __eq__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sum_other = sum(other)
            sum_self = sum(self)
            return True if sum_self == sum_other else False

        else:
            raise ValueError

    def __ne__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sum_other = sum(other)
            sum_self = sum(self)
            return True if sum_self != sum_other else False

        else:
            raise ValueError

    def __gt__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sum_other = sum(other)
            sum_self = sum(self)
            return True if sum_self > sum_other else False

        else:
            raise ValueError

    def __ge__(self, other):
        if isinstance(other, list_pro) or isinstance(other, list):
            sum_other = sum(other)
            sum_self = sum(self)
            return True if sum_self >= sum_other else False

        else:
            raise ValueError


