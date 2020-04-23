import pygame
import random
from colors import *

pygame.init()
# global variables
WIDTH = 400
HEIGHT = 600
FPS = 30
count = 0

# initialization
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("clicker_indev")
pygame.display.set_icon(pygame.image.load('textures/lamp.png').convert_alpha())
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
pygame.time.set_timer(pygame.USEREVENT, 1000)

# load textures, sounds and texts/fonts
FONT = pygame.font.SysFont(None, 20)


#cursor = pygame.image.load("textures/lamp.png")
background = pygame.image.load("textures/background.png").convert_alpha()

pop_sound = [pygame.mixer.Sound("sounds/pop5.wav"),
             pygame.mixer.Sound("sounds/pop6.wav"),
             pygame.mixer.Sound("sounds/pop7.wav")]

class Button(pygame.sprite.Sprite):
    def __init__(self, surfOrTexture, position, group):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(surfOrTexture).convert_alpha()
        except:
            self.size = surfOrTexture[0]
            self.color = surfOrTexture[1]
            self.image = pygame.Surface(self.size)
            self.image.fill(self.color)
        else:
            print("Ошибка загрузки изображения или создания поверхности!")

        self.rect = self.image.get_rect(topleft=position)
        self.add(group)

    def button_pressed(self):
        return self.rect.collidepoint(e.pos)


class Item(Button):
    def __init__(self, rect, text, base_price, base_cps_each):
        self.rect = rect
        self.text = text
        self.count = 0
        self.base_price = base_price
        self.cps_each = base_cps_each

    def draw(self, surface):
        #draw background
        pygame.draw.rect(surface, BLUE, self.rect, 0)
        #draw border
        pygame.draw.rect(surface, BLUE, self.rect, 2)
        #draw text
        text_surface = FONT.render(str(self.count) + "x" + self.text + " $" + str(int(self.price())), False, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        surface.blit(text_surface, text_rect)

    def total_cps(self):
        return self.cps_each * self.count

    def price(self):
        return self.base_price * 1.15**self.count

    def click(self):
        price = self.price()
        global COOKIES
        if COOKIES >= price:
            self.count += 1
            COOKIES -= price

    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def make_items(self, text_list, base_price_list, cps_list, rect, spacing):
        button_height = rect.height / len(text_list)
        button_width = rect.width
        buttons = []
        for i in range(len(text_list)):
            text = text_list[i]
            base_price = base_price_list[i]
            base_cps = cps_list[i]
            button_rect = pygame.Rect(rect.left, rect.top + i * (button_height + spacing), button_width, button_height)
            button = Item(button_rect, text, base_price, base_cps)
            buttons.append(button)
        return buttons

items = Item.make_items(["Cursor", "Grandma", "Farm", "Factory", "Mine", "Shipment", "Alchemy Lab", "Portal",
                    "Time machine", "Antimatter condenser", "Prism"],
                   [15, 100, 500, 3000, 10000, 40000, 200000, 1666666, 123456789, 3999999999, 75000000000],
                   [0.1, 0.5, 4, 10, 40, 100, 400, 6666, 98765, 999999, 10000000],
                   pygame.Rect(70, 30, 230, 400), 5)



game_menu_buttons = pygame.sprite.Group()
store_menu_buttons = pygame.sprite.Group()

cookie = Button("textures/cookie_button.png", [WIDTH//2-135, HEIGHT//2-135], game_menu_buttons)
store = Button(((50, 50), ORANGE), (50, 490), game_menu_buttons)
back = Button(((20, 20), GRAY), (30, 30), store_menu_buttons)

# object and more
#counter_font = TextButton(None, 50, "Счёт: ", colors.LIGHT_BLUE, (30, 30))
#boost_textbutton = TextButton(None, 35, 'Первый бустер ', colors.LIGHT_BLUE, (50, 60))


#cookie = Button([WIDTH//2-135, HEIGHT//2-135], texture_or_surf='textures/cookie_button.png', debug_name='cookie_button')
#store = Button([50, 490], ([50, 50], colors.ORANGE), test=True, debug_name='store_button' )
#back = Button([30, 30], ([20, 20], colors.GRAY), test=True, debug_name='back_button')



full_sc = False
def fullscreen_mode():
    """Полноэкранный режим"""

    global full_sc
    global win

    if not full_sc:
        win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        full_sc = True
    else:
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        full_sc = False





menu_choice = 'game'
def menu(choice):
    """выбор меню игры"""
    if choice == 'game':
        win.fill(WHITE)

        pygame.draw.line(win, GRAY, [0, 0], [WIDTH, 0], 15)
        pygame.draw.line(win, GRAY, [0, 95], [WIDTH, 95], 10)
        pygame.draw.line(win, GRAY, [0, 0], [0, 95], 15)
        pygame.draw.line(win, GRAY, [WIDTH, 0], [WIDTH, 95], 15)

        win.blit(background, (0, 100))

        game_menu_buttons.draw(win)
        pygame.display.update()

    elif choice == 'store':
        win.fill(WHITE)

        store_menu_buttons.draw(win)
        for button in items:
            button.draw(win)
        pygame.display.update()



boost_score = 0
bonus_on = False
while True:
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit()

        if e.type == pygame.KEYDOWN and e.key == pygame.K_f:
            fullscreen_mode()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            # Проверка состояния меню вносится в отдельный if, под которым проверяются нужные кнопки.
            #if menu_choice == 'game':

            if cookie.button_pressed():
                    random.choice(pop_sound).play()
                    count += 1

            if store.button_pressed():
                menu_choice = 'store'
            

            if menu_choice == 'store':

                if back.button_pressed():
                    menu_choice = 'game'
            '''
                if boost_textbutton.button_pressed() and count >= 10:
                    count -= 10
                    boost_score += 1
                    bonus_on = True
            '''

        if bonus_on and e.type == pygame.USEREVENT:
            count += boost_score


# Сделать так, чтобы при нажатии на кнопку та немного уменьшалась в размере.
    print("Cчёт: " + str(count))
    menu(menu_choice)


