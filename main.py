import random
import sys


class Gui:
    difficulty_levels = [
        {
            'name': 'Лёгкий',
            'mine_percent': 0.1,
        },
        {
            'name': 'Средний',
            'mine_percent': 0.2,
        },
        {
            'name': 'Сложный',
            'mine_percent': 0.3,
        },
    ]

    def __init__(self):
        self.width, self.height = [int(i) for i in input('Введите размеры поля в формате WxH: ').split('x')]
        self.board_mines = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.board_opened = [[False for _ in range(self.width)] for _ in range(self.height)]

        self.game_continues = True

        self.level_name = ""
        self.mines = 0

        self.choose_difficulty_level()

        self.generate_board()

        while self.game_continues and not all(all(self.board_opened[y][x] or self.board_mines[y][x] for x in range(self.width)) for y in range(self.height)):
            self.print_board()

            try:
                x, y = map(int, input('Введите координаты открытия в формате "X Y"').split(' '))
                if x < 1 or x > self.width or y < 1 or y > self.height:
                    print('Некорректные координаты')
                    raise ValueError()
                self.open_cell(x - 1, y - 1)
            except ValueError:
                pass

        if self.game_continues:
            print('Вы победили!')

    def set_difficulty_level(self, name, percent):
        self.mines = int(self.width * self.height * percent)
        self.level_name = name

        print(f'Выбран уровень сложности: "{name}"')

    def choose_difficulty_level(self):
        level = Gui.choice(
            'Выберите уровень сложности: ',
            [f'{i["name"]} ({int(i["mine_percent"] * 100)}% мин)' for i in Gui.difficulty_levels]
        )

        if level == -1:
            sys.exit(0)
        self.set_difficulty_level(
            Gui.difficulty_levels[level]['name'],
            Gui.difficulty_levels[level]['mine_percent']
        )

    def generate_board(self):
        mines = self.mines

        while mines > 0 and not all(all(i) for i in self.board_mines):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.board_mines[y][x]:
                mines += 1
            self.board_mines[y][x] = True
            mines -= 1

        if mines > 0:
            print('ERROR! FIX IT! ЛИШНИЕ МИНЫ!!!')

    def print_board(self):
        row = '  ' + (' ' * (len(str(self.height))))
        for i in range(self.width):
            row += f'  {i + 1} '
        print(row)
        print('-' * len(row))

        for y in range(self.height):
            row = f'{" " * (len(str(self.height)) - len(str(y + 1)))}{y + 1} | '
            for x in range(self.width):
                if self.board_opened[y][x]:
                    if self.board_mines[y][x]:
                        row += ' M '
                    else:
                        row += f' {self.number_at(x, y)} '
                else:
                    row += '[ ]'
                row += ' '
            print(row)

    def number_at(self, x, y) -> int:
        res = 0

        for delta_x in [-1, 0, 1]:
            for delta_y in [-1, 0, 1]:
                if delta_x + x < 0 or delta_x + x > self.width - 1 or delta_y + y < 0 or delta_y + y > self.height - 1:
                    continue
                if delta_y == 0 and delta_x == 0:
                    continue
                res += self.board_mines[y + delta_y][x + delta_x]
        return res

    def open_cell(self, x, y):
        if self.board_mines[y][x]:
            self.board_opened[y][x] = True
            self.game_continues = False
            self.print_board()
            print('Вы нашли мину. Игра окончена')
        else:
            self.board_opened[y][x] = True
            if self.number_at(x, y) == 0:
                for delta_x in [-1, 0, 1]:
                    for delta_y in [-1, 0, 1]:
                        if delta_x + x < 0 or delta_x + x > self.width - 1 or delta_y + y < 0 or delta_y + y > self.height - 1:
                            continue
                        if delta_y == 0 and delta_x == 0:
                            continue
                        if self.board_opened[y + delta_y][x + delta_x]:
                            continue
                        self.open_cell(x + delta_x, y + delta_y)

    @staticmethod
    def choice(label: str, variants: list) -> int:
        while True:
            print(label)
            for i in range(len(variants)):
                print(f'{i + 1}. {variants[i]}')
            res = input('> ')
            if not res.isdigit():
                if res == 'q':
                    print('Выход')
                    return -1
                print('Ошибка! Введите только номер')
            elif int(res) < 1 or int(res) > len(variants):
                print(f'Ошибка! Число должно быть от 1 до {len(variants)}')
            else:
                return int(res) - 1


gui = Gui()
