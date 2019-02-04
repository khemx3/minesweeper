from random import randint  # random library
import pygame

pygame.init()  # initialize pygame library


def mine(n, bombs):  # n is for n x n table, bomb = number of bombs
    # we use table to store the lists
    table = create_table(n)
    table = add_bombs(table, bombs)
    table = change_table(table)
    return table


    # nested loop create multi dimension list
def create_table(n):
    return [[0] * n for i in range(n)]


    # create bomb and use as number 9
def add_bombs(table, bombs):
    for i in range(bombs):
        is_bomb = False
        while not is_bomb:
            x = randint(0, len(table) - 1)
            y = randint(0, len(table) - 1)
            if table[x][y] != 9:
                table[x][y] = 9
                is_bomb = True
    return table


    # this function will check the bomb indicate by number 9
def change_table(table):
    for x in range(len(table)):
        for y in range(len(table[x])):
            if table[x][y] == 9:
                table = check_down_left(table, x, y)
                table = check_down_right(table, x, y)
                table = check_down(table, x, y)
                table = check_up_left(table, x, y)
                table = check_up_right(table, x, y)
                table = check_up(table, x, y)
                table = check_left(table, x, y)
                table = check_right(table, x, y)
    return table


def check_down_left(table, x, y):
    if x + 1 < len(table[0]) and y - 1 >= 0:  # make limitation of checking
        if table[x + 1][y - 1] != 9:  # we use 9 to indicate that it is a bomb
            table[x + 1][y - 1] += 1
    return table


def check_down_right(table, x, y):
    if x + 1 < len(table[0]) and y + 1 < len(table):
        if table[x + 1][y + 1] != 9:
            table[x + 1][y + 1] += 1
    return table


def check_down(table, x, y):
    if x + 1 < len(table[0]):
        if table[x + 1][y] != 9:
            table[x + 1][y] += 1
    return table


def check_up_left(table, x, y):
    if x - 1 >= 0 and y - 1 >= 0:
        if table[x - 1][y - 1] != 9:
            table[x - 1][y - 1] += 1
    return table


def check_up_right(table, x, y):
    if x - 1 >= 0 and y + 1 < len(table):
        if table[x - 1][y + 1] != 9:
            table[x - 1][y + 1] += 1
    return table


def check_up(table, x, y):
    if x - 1 >= 0:
        if table[x - 1][y] != 9:
            table[x - 1][y] += 1
    return table


def check_left(table, x, y):
    if y - 1 >= 0:
        if table[x][y - 1] != 9:
            table[x][y - 1] += 1
    return table


def check_right(table, x, y):
    if y + 1 < len(table):
        if table[x][y + 1] != 9:
            table[x][y + 1] += 1
    return table


def print_table(table):
    for i in table:
        print(i)


class Board:  # whole board
    def __init__(self, board):
        self.board = board

    def __repr__(self):
        return print_table(self.board)


class Square:  # every thing in board
    def __init__(self, x, y, width, height, board, ij):
        self.rect = pygame.rect.Rect(x, y, width, height)
        i, j = ij  # both i and j is equal
        self.val = board[i][j]  # if it is 9 = bomb
        self.x = x
        self.y = y
        self.visible = False  # visible is it is not open yet
        self.flag = False  # to destroy bombs


def restart(size, bombs):
    # restart a game with same size
    game(size, bombs)


# if we open a zero box it will open the box around
def open_space(pick, box):
    box.visible = True
    i, j = box.x // 40, box.y // 40
    if i + 1 < len(pick):
        # we check one cube around the current if its in the table and not visible it will open around and around
        if pick[i + 1][j].visible == False and pick[i + 1][j].flag == False:  # not open yet and no flag on
            pick[i + 1][j].visible = True  # open on [i+1][j]
            if pick[i + 1][j].val == 0:  # check if it is 0
                open_space(pick, pick[i + 1][j])  # recursive checking r to open more space

        if j + 1 < len(pick):  # the rest do the same
            if pick[i + 1][j + 1].visible == False and pick[i + 1][j + 1].flag == False:
                pick[i + 1][j + 1].visible = True
                if pick[i + 1][j + 1].val == 0:
                    open_space(pick, pick[i + 1][j + 1])
        if j - 1 >= 0:
            if pick[i - 1][j - 1].visible == False and pick[i - 1][j - 1].flag == False:
                pick[i - 1][j - 1].visible = True
                if pick[i - 1][j - 1].val == 0:
                    open_space(pick, pick[i - 1][j - 1])

    if i - 1 >= 0:
        if pick[i - 1][j].visible == False and pick[i - 1][j].flag == False:
            pick[i - 1][j].visible = True
            if pick[i - 1][j].val == 0:
                open_space(pick, pick[i - 1][j])

        if j + 1 < len(pick):
            if pick[i - 1][j + 1].visible == False and pick[i - 1][j + 1].flag == False:
                pick[i - 1][j + 1].visible = True
                if pick[i - 1][j + 1].val == 0:
                    open_space(pick, pick[i - 1][j + 1])

        if j - 1 >= 0:
            if pick[i - 1][j - 1].visible == False and pick[i - 1][j - 1].flag == False:
                pick[i - 1][j - 1].visible = True
                if pick[i - 1][j - 1].val == 0:
                    open_space(pick, pick[i - 1][j - 1])

    if j - 1 >= 0:
        if pick[i][j - 1].visible == False and pick[i][j - 1].flag == False:
            pick[i][j - 1].visible = True
            if pick[i][j - 1].val == 0:
                open_space(pick, pick[i][j - 1])

    if j + 1 < len(pick):
        if pick[i][j + 1].visible == False and pick[i][j + 1].flag == False:
            pick[i][j + 1].visible = True
            if pick[i][j + 1].val == 0:
                open_space(pick, pick[i][j + 1])



def game(size, bombs):
    # import song .ogg
    click = pygame.mixer.Sound('button.ogg')
    boom = pygame.mixer.Sound('boom.ogg')
    again = pygame.mixer.Sound('again.ogg')

    # import pictures big one
    white = pygame.image.load("white.jpeg")
    grey = pygame.image.load("grey.jpg")

    #  import pictures with number and bomb and flag
    blank = pygame.image.load("blank.jpeg")
    one = pygame.image.load("one.jpg")
    two = pygame.image.load("two.png")
    three = pygame.image.load("three.jpg")
    four = pygame.image.load("four.jpg")
    five = pygame.image.load("five.jpg")
    six = pygame.image.load("six.png")
    seven = pygame.image.load("seven.jpg")
    eight = pygame.image.load("eight.jpg")
    bomb = pygame.image.load("bomb.png")
    crossbomb = pygame.image.load("crossbomb.png")
    flag = pygame.image.load("flag.png")

    numbers = [blank, one, two, three, four, five, six, seven, eight, bomb]

    a = Board(mine(size, bombs))  # create the board
    width = height = len(a.board) * 40  # size of the screen

    screen = pygame.display.set_mode((width, height))
    # create a list of all squares organized as board
    pick = [[] for i in range(size)]
    for i in range(0, size * 40, 40):
        for j in range(0, size * 40, 40):  # generate grey pictures
            pick[i // 40] += [Square(i, j, 40, 40, a.board, (i // 40, j // 40))]
            screen.blit(grey, (i, j))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # press 'r' to restart
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    again.play()
                    run = False
                    restart(size, bombs)
            # left click to resolve
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in pick:
                    for j in i:
                        # check which square is pressed
                        r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                        if j.rect.colliderect(r):  # if mouse and current Square are in the same
                            click.play()
                            if j.flag == False:  # if current square have flag we can't press it.
                                if j.val == 9:  # 9 is a bomb
                                    boom.play()
                                    print("game over!!!")
                                    run = False
                                j.visible = True
                                if j.val == 0:
                                    j.visible = open_space(pick, j)
                                    j.visible = True

            # right click to deploy flag
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for i in pick:
                    for j in i:
                        r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                        click.play()
                        if j.rect.colliderect(r):
                            # flag on and off
                            if j.visible == False:
                                if j.flag == False:
                                    j.flag = True
                                elif j.flag == True:
                                    j.flag = False
        for i in pick:
            for j in i:
                if j.visible == True:
                    screen.blit(white, (j.x, j.y))
                    screen.blit(numbers[j.val], (j.x + 10, j.y + 10))
                    # show out number picture base on current board value

                if j.flag == True:
                    screen.blit(flag, (j.x + 10, j.y + 10))
                if j.flag == False and j.visible == False:
                    screen.blit(grey, (j.x, j.y))

        # check for how many bombs left
        count = 0
        for i in pick:
            for j in i:
                if j.visible == True and j.val != 9:
                    count += 1
            # no bombs left = win
            if count == size * size - bombs:
                run = False  # end game
                print("you win!!!")
        pygame.display.update()

    # if win or lose reveal all bomb
    for i in pick:
        for j in i:
            if j.val == 9 and j.flag == True:  # val = 9 is bombs
                screen.blit(crossbomb, (j.x + 10, j.y + 10))  # show all bombs
            elif j.val == 9 and j.flag == False:
                screen.blit(bomb, (j.x + 10, j.y + 10))

    pygame.display.update()

    run = True  # game still on..
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if we close then game off
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:  # if we press r it will restart
                if event.key == pygame.K_r:
                    again.play()  # sound on
                    run = False
                    restart(size, bombs)


def mainmenu():
    background = pygame.image.load("background.jpg")
    start = pygame.image.load("start.png")
    option = pygame.image.load("option.png")
    logo = pygame.image.load("Minesweepers.png")
    quitpic = pygame.image.load("quit.png")

    screen = pygame.display.set_mode((960, 600))
    screen.blit(background, (1, 1))
    screen.blit(logo, (152, 45))
    screen.blit(start, (380, 150))
    screen.blit(option, (380, 250))
    screen.blit(quitpic, (420, 400))
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect((380, 150), (200, 78)).collidepoint(event.pos):
                    game(5, 5)

                elif pygame.Rect((380, 250), (200, 50)).collidepoint(event.pos):
                    mode()

                elif pygame.Rect((420, 400), (200, 50)).collidepoint(event.pos):
                    pygame.quit()

        pygame.display.update()


def mode():
    background = pygame.image.load("background.jpg")
    easy = pygame.image.load("easy.png")
    normal = pygame.image.load("normal.png")
    hard = pygame.image.load("inhuman.png")

    screen = pygame.display.set_mode((960, 600))
    screen.blit(background, (1, 1))
    screen.blit(easy, (350, 45))
    screen.blit(normal, (350, 115))
    screen.blit(hard, (350, 200))
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect((350, 45), (184, 63)).collidepoint(event.pos):
                    game(6, 5)
                elif pygame.Rect((350, 115), (276, 63)).collidepoint(event.pos):
                    game(10, 20)
                elif pygame.Rect((350, 200), (300, 63)).collidepoint(event.pos):
                    game(10, 40)

        pygame.display.update()


mainmenu()
