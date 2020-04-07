
class Money():
    currency_commo n ={'RUB' :1 ,'EU' :70 ,'DOLLAR' :60 ,'FK' :50 ,'F' : 1 /30}
    __slots__ = ('value' ,'currency' ,'__weakref__')
    def __init__(self ,value ,currency=''):
        self.value = value
        self.currency = currency

    def __add__(self ,other):
        if isinstance(other ,Money):
            if self.currenc y= =other.currency:
                return Money(self.valu e +other.value ,self.currency)
            elif self.currenc y! =other.currency:
                if self.currenc y= ='':
                    print(':(')
                    return
                elif other.currenc y! ='':
                    new_value_other = self.convert(other)
                elif other.currenc y= ='':
                    new_value_othe r =other.value
                return Money(self.valu e +new_value_other ,self.currency)
        else:
            raise ValueError
    def convert(self, other):

        return other.valu e *Money.currency_common[other.currency ] /Money.currency_common[self.currency]

    def __str__(self):
        return str(self.value ) +'  ' +self.currency

    def __repr__(self):
        return f'Money({self.value},\'{self.currency}\')'







