import pygame
import time
from random import randint
import sys

#settings#
mines = 20
rows = 15
cols = 15
game_status = 1
victory = 0
#settings#


sys.setrecursionlimit(10000) #needed for bubbling

start_time = time.time()

pygame.init()

clock = pygame.time.Clock()

field = pygame.image.load('field.bmp')
field_hover = pygame.image.load('field_hover.bmp')

flag = pygame.image.load('flag.bmp')
flag_hover = pygame.image.load('flag_hover.bmp')

question = pygame.image.load('question.bmp')
question_hover = pygame.image.load('question_hover.bmp')

mine = pygame.image.load('mine.bmp')

empty = pygame.image.load('empty.bmp')

i1 = pygame.image.load('1.bmp')
i2 = pygame.image.load('2.bmp')
i3 = pygame.image.load('3.bmp')
i4 = pygame.image.load('4.bmp')
i5 = pygame.image.load('5.bmp')
i6 = pygame.image.load('6.bmp')
i7 = pygame.image.load('7.bmp')
i8 = pygame.image.load('8.bmp')


class Field:

    #total count of fields
    counter = 0
    #size of side
    field_size = 16
    #which field types can be revealed in chain
    bubblable_types = ['Empty', 'Indice']

    def __init__(self, x, y):

        self.id = Field.counter
        Field.counter +=1

        #'Empty' or 'Mine' or 'Indice'
        self.type = 'Empty'
        #'Clickable' or 'Triggered'
        self.state = 'Clickable'
        #how many mines are around, if it is not mine field
        self.indice = 0

        #can trigger revealing in chain
        self.is_bubbling = False

        #default block image
        self.image = field

        #coordinates of field
        self.position = {'start': {}, 'end': {}}
        self.position['start']['x'] = x
        self.position['start']['y'] = y
        self.position['end']['x'] = x + self.field_size
        self.position['end']['y'] = y + self.field_size

    #construct image on screen
    def update(self):

        gameDisplay.blit(self.image, (self.position['start']['x'], self.position['start']['y']))

    #highligh of field
    def hover(self, event):
        if self.state == 'Clickable':
            if mouse_target(self, event):
                self.image = field_hover
            else:
                self.image = field

        elif self.state == 'Flag':
            if mouse_target(self, event):
                self.image = flag_hover
            else:
                self.image = flag

        elif self.state == 'Question':
            if mouse_target(self, event):
                self.image = question_hover
            else:
                self.image = question

    #called by lmb or bubble()
    def trigger(self, bubbling = False):

        global game_status
        global clicks

        self.state = 'Triggered'

        if self.type == 'Empty':
            self.image = empty
        elif self.type == 'Mine':
            self.image = mine
            game_status = 0
        elif self.type == 'Indice':
            if self.indice == 1:
                self.image = i1
            elif self.indice == 2:
                self.image = i2
            elif self.indice == 3:
                self.image = i3
            elif self.indice == 4:
                self.image = i4
            elif self.indice == 5:
                self.image = i5
            elif self.indice == 6:
                self.image = i6
            elif self.indice == 7:
                self.image = i7
            elif self.indice == 8:
                self.image = i8

        if self.type != 'Mine':
            clicks += 1

        bubble(self.id)

    #left mouse button
    def lmb(self, event):
        if self.state == 'Clickable' or self.state == 'Question':
            if mouse_target(self, event) and event.button == 1:

                self.trigger()

    #right mouse button
    def rmb(self, event):
        if self.state == 'Clickable':
            if mouse_target(self, event):
                self.state = 'Flag'
                self.image = flag
        elif self.state == 'Flag':
            if mouse_target(self, event):
                self.state = 'Question'
                self.image = question
        elif self.state == 'Question':
            if mouse_target(self, event):
                self.state = 'Clickable'
                self.image = field

    def set_bubbling(self):
        for bubbling_type in self.bubblable_types:
            if self.type == bubbling_type:
                self.is_bubbling = True
                break

    def disable_bubbling(self):
        self.is_bubbling = False

#/FIELD

#check mouse is on field's coordinates
def mouse_target(field, event):
        return field.position['start']['x'] <= event.pos[0] <= field.position['end']['x'] and field.position['start']['y'] <= event.pos[1] <= field.position['end']['y']

def bubble(index):

    if (fields[index].is_bubbling):

        fields[index].disable_bubbling()

        if (fields[index].type == 'Empty'):
            if is_on(Field.bubblable_types, 'L', index) and fields[index - 1].state != 'Triggered':
                fields[index - 1].trigger()
            if is_on(Field.bubblable_types, 'R', index) and fields[index + 1].state != 'Triggered':
                fields[index + 1].trigger()
            if is_on(Field.bubblable_types, 'T', index) and fields[index - cols].state != 'Triggered':
                fields[index - cols].trigger()
            if is_on(Field.bubblable_types, 'D', index) and fields[index + cols].state != 'Triggered':
                fields[index + cols].trigger()

            if is_on(Field.bubblable_types, 'LT', index) and fields[index - cols - 1].state != 'Triggered':
                fields[index - cols - 1].trigger()
            if is_on(Field.bubblable_types, 'RT', index) and fields[index - cols + 1].state != 'Triggered':
                fields[index - cols + 1].trigger()
            if is_on(Field.bubblable_types, 'LD', index) and fields[index + cols - 1].state != 'Triggered':
                fields[index + cols - 1].trigger()
            if is_on(Field.bubblable_types, 'RD', index) and fields[index + cols + 1].state != 'Triggered':
                fields[index + cols + 1].trigger()

pygame.display.set_caption('Mine sweeper')

fields = []
clicks_to_victory = rows * cols - mines
clicks = 0

#ADJUSTING SIZES FOR SMALL GAMEBOARD
if cols <= 10:
    font_size = 15
    FOOTER_HEIGHT = 25
    FOOTER_PADDING = 5
else:
    font_size = 30
    FOOTER_HEIGHT = 50
    FOOTER_PADDING = 10

#COMPUTING WINDOW SIZE
WINDOW_WIDTH = (Field.field_size + 1) * cols - 1
WINDOW_HEIGHT = (Field.field_size + 1) * rows - 1 + FOOTER_HEIGHT

footer = pygame.Rect(0,WINDOW_HEIGHT - FOOTER_HEIGHT,WINDOW_WIDTH,FOOTER_HEIGHT)
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

timer_font = pygame.font.SysFont('Verdana', font_size)
summary_font = pygame.font.SysFont('Verdana', 30)

#FILLING FIELDS
row = 0
col = 0
while row < rows:
    while True:
        fields.append(Field(col * 17, row * 17))
        col += 1
        if col == cols:
            col = 0
            break
    row += 1

#FILLING MINES
if not mines >= Field.counter:
    ammo = mines
    i = 0
    while ammo:

        if not randint(0, (Field.counter - 1)):
            if fields[i].type != 'Mine':
                fields[i].type = 'Mine'
                ammo -= 1
        
        i +=1
        if i == Field.counter:
            i = 0
else:
    raise Exception("Too many mines selected for actual size.")

#CHECK MINE TYPE RELATIVELY
def is_on(field_types, position, index):

#CAN TAKE ARRAY OF TYPES OR SINGLE TYPE
    def check_types_array(where):
        if isinstance(field_types, str):
            return fields[where].type == field_types
        else:
            for field_type in field_types:
                if fields[where].type == field_type:
                    return True

    if (position == 'L'):
        return index % cols != 0 and check_types_array(index - 1)
    elif (position == 'R'):
        return (index + 1) % cols != 0 and check_types_array(index + 1)
    elif (position == 'T'):
        return index >= cols and check_types_array(index - cols)
    elif (position == 'D'):
        return not index + cols >= Field.counter and check_types_array(index + cols)
    elif (position == 'LT' or position == 'TL'):
        return index % cols != 0 and index >= cols and check_types_array(index - cols - 1)
    elif (position == 'RT' or position == 'TR'):
        return (index + 1) % cols != 0 and index >= cols and check_types_array(index - cols + 1)
    elif (position == 'LD' or position == 'DL'):
        return index % cols != 0 and not index + cols >= Field.counter and check_types_array(index + cols - 1)
    elif (position == 'RD' or position == 'DR'):
        return (index + 1) % cols != 0 and not index + cols >= Field.counter and check_types_array(index + cols + 1)


#FILLING INDICES
def indices_filler(i):

    nearby_mines = 0

    if fields[i].type != 'Mine':
        if is_on('Mine', 'L', i):
            nearby_mines += 1
        if is_on('Mine', 'R', i):
            nearby_mines += 1
        if is_on('Mine', 'T', i):
            nearby_mines += 1
        if is_on('Mine', 'D', i):
            nearby_mines += 1
        if is_on('Mine', 'LT', i):
            nearby_mines += 1
        if is_on('Mine', 'RT', i):
            nearby_mines += 1
        if is_on('Mine', 'LD', i):
            nearby_mines += 1
        if is_on('Mine', 'RD', i):
            nearby_mines += 1

    if nearby_mines > 0:
        fields[i].type = 'Indice'
        fields[i].indice = nearby_mines

i = 0
while i < Field.counter:
    indices_filler(i)
    i += 1
#/FILLING INDICES
#SETS BUBBLING
list(map(lambda x:x.set_bubbling(), fields))

#GAME LOOP
while game_status:

    #events
    for event in pygame.event.get():

        #mouse hover
        if event.type == pygame.MOUSEMOTION:

            list(map(lambda x:x.hover(event), fields))

        #mouse clicks
        if event.type == pygame.MOUSEBUTTONUP:
            
            if event.button == 1:
                list(map(lambda x:x.lmb(event), fields))
            elif event.button == 3:
                list(map(lambda x:x.rmb(event), fields))

        if event.type == pygame.QUIT:
            game_status = 0

    if clicks == clicks_to_victory:
        game_status = 0
        victory = 1

    gameDisplay.fill((0,0,0))

    list(map(lambda x:x.update(),fields))

    pygame.draw.rect(gameDisplay, (180,180,180), footer)

    active_time = int(time.time() - start_time)

    textsurface = timer_font.render('Time: ' + str(active_time), False, (0, 0, 0))

    gameDisplay.blit(textsurface,(FOOTER_PADDING, WINDOW_HEIGHT - FOOTER_HEIGHT + 5))

    pygame.display.update()
    clock.tick(60)

total_time = int(time.time() - start_time)
#SHOW ALL MINES
list(map(lambda x:x.trigger(),fields))

resume = 1

#END LOOP
while resume:
    check = 0

    #events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            resume = 0


    gameDisplay.fill((0,0,0))

    if victory:
        pygame.draw.rect(gameDisplay, (100,255,100), footer)
    else:
        pygame.draw.rect(gameDisplay, (255,100,100), footer)

    list(map(lambda x:x.update(),fields))

    textsurface = timer_font.render('Time: ' + str(total_time), False, (0, 0, 0))

    gameDisplay.blit(textsurface,(FOOTER_PADDING, WINDOW_HEIGHT - FOOTER_HEIGHT + 5))

    pygame.display.update()


pygame.quit()
quit()