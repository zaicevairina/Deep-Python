
class Hall:

    def load(self,path=None):
        try:
            with open(path) as file:
                self.map = []
                for i, line in enumerate(file):
                    line = line.split('\n')[0].split(' ')
                    self.map.append(line)
            self.count_row = len(self.map)
            self.count_place = len(self.map[0])
        except FileNotFoundError:
            print('try again, file does not exist')


    def check_place(self,row,place):
        if row>self.count_row  or place>self.count_place:
            return f'place {row,place} does not exist'
        if self.map[row-1][place-1]=='0':
            return f'place {row,place} is free'
        else:
            return f'place {row,place} taken'

    def check_free(self):
        k=0
        for i in range(self.count_row):
            for j in range(self.count_place):
                if self.map[i][j]=='0':
                    k+=1
        return k

    def __str__(self):
        x = ''
        for i in range(self.count_row):
            for j in range(self.count_place):
                x+=self.map[i][j]+' '
            x+='\n'
        return x[:-1]

h = Hall()
h.load('place.txt')
print(h)
print(h.check_place(5,1))
print(h.check_free())
