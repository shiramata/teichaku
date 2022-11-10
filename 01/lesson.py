class Person:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
    
    def eat_lunch(self, food):
        if food == 'rice':
            print('おなかいっぱい')
        elif food == 'bread':
            print('パンは嫌い')


ogawa = Person(name = 'Tokuya', strategy = 'goo')
kubo = Person(name = 'Hidaka', strategy = 'choki')

def battle(person1, person2):
    table = {
        # win: lose
        'goo': 'choki',
        'choki': 'par',
        'par': 'goo'
    }
    if table[person1.strategy] == person2.strategy:
        print(f'{person1.name} won! strategy: {person1.strategy}')
    elif table[person2.strategy] == person1.strategy:
        print(f'{person2.name} won! strategy: {person2.strategy}')
    else:
        print('aiko!')

if __name__ == '__main__':
    battle(person1=ogawa, person2=kubo)
    ogawa.eat_lunch(food='udon')