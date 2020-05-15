class Money():
    currency_common = {'RUB': 1, 'EU': 70, 'DOLLAR': 60, 'FK': 50, 'F': 1 / 30}
    __slots__ = ('value', 'currency', '__weakref__')

    def __init__(self, value, currency=''):
        self.value = value
        self.currency = currency

    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(self.value + other.value, self.currency)
            elif self.currency != other.currency:
                if self.currency == '':
                    print(':(')
                    return
                elif other.currency != '':
                    new_value_other = self.convert(other)
                elif other.currency == '':
                    new_value_other = other.value
                return Money(self.value + new_value_other, self.currency)
        elif isinstance(other, int):
            return Money(self.value + other, self.currency)

        else:
            raise ValueError

    def __str__(self):
        return str(self.value) + '  ' + self.currency

    def __repr__(self):
        return f'Money({self.value},\'{self.currency}\')'

    def convert(self, other):

        return other.value * Money.currency_common[other.currency] / Money.currency_common[self.currency]


print("Сложение")
a = Money(1, 'RUB')
b = Money(1, 'EU')
print(f'{a} + {b} = {a + b}')
print(a, ',', b)

print('-' * 10)
a = Money(1, 'EU')
b = Money(70, 'RUB')
print(f'{a} + {b} = {a + b}')
print(a, ',', b)

print('-' * 10)
a = Money(1, 'RUB')
b = Money(1)
print(f'{a} + {b} = {a + b}')
print(a, ',', b)

print('-' * 10)
a = Money(1, 'RUB')
b = 1
print(f'{a} + {b} = {a + b}')
print(a, ',', b)

print('-' * 10)
print("переопределение repr")
x = eval(repr(Money(1,'DOLLAR')))
print(x,',', type(x))
