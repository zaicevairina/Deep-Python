import sqlite3


class CharField:

    def __init__(self):
        self.obj = None

    def __set__(self, obj, val):
        if isinstance(val, str):
            self.obj = val
        else:
            raise TypeError

    def __get__(self, obj, objtype):
        return self.obj

    def __delete__(self, obj):
        del self.obj


class IntegerField:

    def __init__(self):
        self.obj = None

    def __set__(self, obj, val):
        if isinstance(val, int):
            self.obj = val
        else:
            raise TypeError

    def __get__(self, obj, objtype):
        return self.obj

    def __delete__(self, obj):
        del self.obj


class Base:
    attrs = []

    @classmethod
    def connect(cls, database):
        cls.conn = sqlite3.connect(database)
        cls.cursor = cls.conn.cursor()

    @classmethod
    def get_attr(cls):
        return list(set(dir(cls)) - set(dir(Base)))

    @classmethod
    def create_table(cls):
        query = f"CREATE TABLE {cls.__name__} ("
        cls.attrs = cls.get_attr()
        for attr in cls.attrs:
            if 'IntegerField' in str(cls.__dict__[attr]):
                type_attr = 'int'
            elif 'CharField' in str(cls.__dict__[attr]):
                type_attr = 'text'
            query += '{} {},'.format(attr, type_attr)
        query = query[:-1] + ')'
        try:
            cls.cursor.execute(query)
        except sqlite3.OperationalError:
            print(f'Table {cls.__name__} already exists')

    @classmethod
    def create(cls, **kwargs):

        query = "INSERT INTO {} (".format(cls.__name__)
        cls.attrs = cls.get_attr()
        try:
            cls.attrs.remove('Foo')
        except:
            pass
        for column in cls.attrs:
            query += f'{column},'
        query = query[:-1] + ') VALUES ('
        if kwargs is not None and len(kwargs.keys()) == len(cls.attrs):
            for attr in cls.attrs:
                if isinstance(kwargs[attr], str):
                    query += '\'{}\','.format(kwargs[attr])
                else:
                    query += '{},'.format(kwargs[attr])

            query = query[:-1] + ')'
        cls.cursor.execute(query)
        cls.conn.commit()

        dict_attrs = dict.fromkeys(cls.attrs)
        dict_attrs.update({'update': cls.update})
        cls.Foo = type(f'{cls.__name__}', (cls,), dict_attrs)
        x = cls.Foo()

        if kwargs is not None and len(kwargs.keys()) == len(cls.attrs):
            for attr in cls.attrs:
                if isinstance(kwargs[attr], str):
                    exec(f'x.{attr} = \'{kwargs[attr]}\'')
                else:
                    exec(f'x.{attr} = {kwargs[attr]}')

        return x

    @classmethod
    def all(cls):
        query = f'SELECT * FROM {cls.__name__}'
        cls.cursor.execute(query)
        return cls.cursor.fetchall()

    @classmethod
    def get(cls, **kwargs):
        query = f'SELECT * FROM {cls.__name__} WHERE '
        for key, value in kwargs.items():
            if isinstance(value, int):
                query += f'{key}={value} AND '
            elif isinstance(value, str):
                query += f'{key}=\'{value}\' AND '

        query = query[:-4]
        cls.cursor.execute(query)
        return cls.cursor.fetchall()

    def update(self, **kwargs):
        query = f'UPDATE {self.__class__.__name__} SET '

        for key, value in kwargs.items():
            if isinstance(value, int):
                query += f'{key}={value} AND '
            elif isinstance(value, str):
                query += f'{key}=\'{value}\' AND '

        query = query[:-4]
        query += 'WHERE '
        for attr in self.__class__.attrs:
            value = eval(f'self.{attr}')
            if isinstance(value, int):
                query += f'{attr}={value} AND '
            elif isinstance(value, str):
                query += f'{attr}=\'{value}\' AND '
        query = query[:-4]

        self.__class__.cursor.execute(query)
        self.__class__.conn.commit()

    @classmethod
    def delete(cls, **kwargs):
        query = f'DELETE FROM {cls.__name__} WHERE '

        for key, value in kwargs.items():
            if isinstance(value, int):
                query += f'{key}={value} AND '
            elif isinstance(value, str):
                query += f'{key}=\'{value}\' AND '

        query = query[:-4]

        cls.cursor.execute(query)
        cls.conn.commit()

    def __str__(self):
        answer = ''
        for attr in self.__class__.attrs:
            value = eval(f'self.{attr}')
            if isinstance(value, int):
                answer += f'{attr}={value} '
            elif isinstance(value, str):
                answer += f'{attr}=\'{value}\' '
        return answer


class Person(Base):
    id = IntegerField()
    name = CharField()
    age = IntegerField()


class City(Base):
    name_city = CharField()
    id_city = IntegerField()
    country = CharField()


db = 'database.db'
Base.connect(db)

City.create_table()
City1 = City.create(name_city='Moskow', id_city=111, country='Russia')
City2 = City.create(name_city='Saratov', id_city=222, country='Russia')
City3 = City.create(name_city='Kiev', id_city=333, country='Ukrain')

Person.create_table()
Person1 = Person.create(id=1, name='Masha', age=20)
Person2 = Person.create(id=2, name='Pasha', age=30)
Person3 = Person.create(id=3, name='Masha', age=40)

print('вывод таблицы Person')
print(Person.all(), '\n')

print('вывод таблицы City')
print(City.all(), '\n')

print('получить людей с id=2 и именем Pasha ')
print(Person.get(id=2, name='Pasha'), '\n')

print('получить людей с именем Masha')
print(Person.get(name='Masha'), '\n')

print('обновили id у Masha(person1) и выводим всю таблицу')
Person1.update(id=6)
print(Person.all(), '\n')

print('удалили пользователя с id=5 и выводим всю таблицу')
Person.delete(id=5)
print(Person.all(), '\n')

print('удалили пользователя с id=6 и выводим всю таблицу')
Person.delete(id=6)
print(Person.all(), '\n')

print('вывод таблицы City')
print(City.all(), '\n')
print(City1)
print(City2)
