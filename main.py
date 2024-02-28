from os import path, listdir
from random import choice
from math import radians, cos, sin, pi
from sys import exit
import pygame
import pygame_gui

pygame.init()

TILE_SIZE = 64
SCREEN_INFO = pygame.display.Info()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = SCREEN_INFO.current_w, SCREEN_INFO.current_h
MAPS_DIR = "maps"
MAPS_NUM = 1
FPS = 60
screen = pygame.display.set_mode(WINDOW_SIZE)


def load_image(name, colorkey=None):
    fullname = path.join('data', name)
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["СПАСИБО, ЧТО ЗАПУСТИЛИ ЭТОТ ШЕДЕВР",
                  "Правила игры:",
                  "Ваша задача - сломать все плохие шарики",
                  "Управление платформой - мышка",
                  "Запуск вашего шарика - SPACE или ЛКМ",
                  "Рестарт вашего шарика - клавиша R",
                  "Выход из игры - ESCAPE",
                  "Для продолжения нажмите любую кнопку",
                  "(Читы: клавиша D - удаление всех шаров)"]

    background = pygame.transform.scale(load_image('start_screen.jpg'), WINDOW_SIZE)
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 36)
    text_coord = 550
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 600
        text_coord += intro_rect.height + 7
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    exit()


def pause():
    field = pygame.Surface([600, 300])
    field.fill('grey')
    screen.blit(field, (WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 150))
    pygame.mouse.set_visible(True)
    text = ["PAUSE", "Press SPACE to resume"]
    font = pygame.font.Font(None, 60)
    text_coord = WINDOW_HEIGHT // 2 - 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WINDOW_WIDTH // 2 - 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mouse.set_visible(False)
                return
        pygame.display.flip()
        clock.tick(FPS)


def show_win_message():
    global moving, MAPS_NUM, board
    pygame.mouse.set_visible(True)

    background = pygame.transform.scale(load_image('win_screen.jpg'), WINDOW_SIZE)

    font = pygame.font.Font(None, 120)
    text = font.render("YOU WON", 1, "darkblue")

    manager = pygame_gui.UIManager(WINDOW_SIZE)

    exit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 550), (300, 100)),
                                          text='Exit',
                                          manager=manager)

    restart = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 700), (300, 100)),
                                           text='Restart',
                                           manager=manager)

    next_level = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 700), (300, 100)),
                                           text='Next level',
                                           manager=manager)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit:
                        terminate()
                    if event.ui_element == restart:
                        moving = False
                        pygame.mouse.set_visible(False)
                        player.angle = radians(45 + 90 * choice([0, 1]))
                        board.render()
                        pygame.mixer.music.load("sounds/bk_music.mp3")
                        pygame.mixer.music.play(-1)
                        return
                    if event.ui_element == next_level:
                        MAPS_NUM = (MAPS_NUM + 1) % len(listdir('maps/'))
                        moving = False
                        player.angle = radians(45 + 90 * choice([0, 1]))
                        pygame.mouse.set_visible(False)
                        board = Board(f"map_{MAPS_NUM}.txt")
                        board.render()
                        pygame.mixer.music.load("sounds/bk_music.mp3")
                        pygame.mixer.music.play(-1)
                        return
            manager.process_events(event)
        manager.update(clock.tick(FPS) / 1000)
        screen.blit(background, (0, 0))
        screen.blit(text, (1000, 100))
        manager.draw_ui(screen)
        pygame.display.update()


def show_lose_message():
    global moving, board
    pygame.mouse.set_visible(True)

    background = pygame.transform.scale(load_image('lose_screen.jpg'), WINDOW_SIZE)

    font = pygame.font.Font(None, 120)
    text = font.render("YOU LOSE", 1, "darkblue")

    manager = pygame_gui.UIManager(WINDOW_SIZE)

    exit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 400), (300, 100)),
                                          text='Exit',
                                          manager=manager)

    restart = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 550), (300, 100)),
                                           text='Restart',
                                           manager=manager)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit:
                        terminate()
                    if event.ui_element == restart:
                        moving = False
                        pygame.mouse.set_visible(False)
                        player.angle = radians(45 + 90 * choice([0, 1]))
                        board = Board(f"map_{MAPS_NUM}.txt")
                        board.render()
                        pygame.mixer.music.load("sounds/bk_music.mp3")
                        pygame.mixer.music.play(-1)
                        return
            manager.process_events(event)
        manager.update(clock.tick(FPS) / 1000)
        screen.blit(background, (0, 0))
        screen.blit(text, (50, 150))
        manager.draw_ui(screen)
        pygame.display.update()


def check_win():
    if not all_balls.sprites():
        return True


def check_lose():
    if player.rect.bottom > platform.rect.bottom:
        return True


class Ball(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("ball.png"), (TILE_SIZE, TILE_SIZE))
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.radius = TILE_SIZE // 2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self, filename):
        self.map = []
        with open(path.join(MAPS_DIR, filename)) as input_file:
            for line in input_file:
                self.map.append((list(map(int, line.split()))))
        self.tile_size = TILE_SIZE
        self.height = len(self.map)

    def render(self):
        for y in range(self.height):
            for x in range(len(self.map[y])):
                if self.get_tile_id((x, y)):
                    ball = Ball(x * TILE_SIZE, y * TILE_SIZE)
                    all_balls.add(ball)
                    all_sprites.add(ball)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface([200, 20], pygame.SRCALPHA, 32)
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)

    def update(self):
        self.rect.center = (pygame.mouse.get_pos()[0], WINDOW_HEIGHT - 50)


class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('player.png'), (TILE_SIZE // 2, TILE_SIZE // 2))
    def __init__(self):
        super().__init__(all_sprites)
        self.angle = radians(45 + 90 * choice([0, 1]))
        self.radius = TILE_SIZE // 4
        self.v = 10
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.center = (platform.rect.center[0], platform.rect.center[1] - self.rect.height // 2 + 1)

    def update(self):
        if not moving:
            self.rect.center = (platform.rect.center[0], platform.rect.center[1] - self.rect.height // 2 - 10)
        else:
            x, y = self.rect.center
            self.rect.center = (x + self.v * cos(self.angle), y - self.v * sin(self.angle))
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.angle = -self.angle
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.angle = pi - self.angle
            if pygame.sprite.collide_rect(self, platform):
                coef = (x - platform.rect.center[0]) / (platform.rect.width / 2)
                if coef > 1:
                    coef = (self.rect.x - platform.rect.center[0]) / (platform.rect.width / 2)
                elif coef < -1:
                    coef = (self.rect.right - platform.rect.center[0]) / (platform.rect.width / 2)
                if 0.0 <= coef < 0.3:
                    coef = 0.3
                elif coef < -0.7:
                    coef = -0.7
                if coef > 0:
                    self.angle = radians(90 * abs(coef))
                else:
                    self.angle = radians(90 + 90 * abs(coef))
            hits = pygame.sprite.spritecollide(self, all_balls, False)
            if hits:
                for ball in hits:
                    if pygame.sprite.collide_circle(self, ball):
                        x_b, y_b = ball.rect.x, ball.rect.y
                        if x_b <= x <= x_b + TILE_SIZE:
                            self.angle = -self.angle
                        else:
                            self.angle = pi - self.angle
                        ball.kill()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == '__main__':

    pygame.display.set_caption('Арканоид на pygame ver 1.0.')
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    backgroud = pygame.transform.scale(load_image('background.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))

    start_screen()

    all_sprites = pygame.sprite.Group()
    all_balls = pygame.sprite.Group()
    board = Board(f"map_{MAPS_NUM}.txt")
    board.render()

    platform = Platform()
    player = Player()

    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()


    Border(1, 0, WINDOW_WIDTH, 0)
    Border(0, WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
    Border(0, 0, 0, WINDOW_HEIGHT)
    Border(WINDOW_WIDTH, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    pygame.mixer.music.load("sounds/bk_music.mp3")
    pygame.mixer.music.play(-1)

    running = True
    moving = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                moving = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                moving = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.mixer.music.pause()
                pause()
                pygame.mixer.music.unpause()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                for ball in all_balls:
                    ball.kill()
        if check_win():
            pygame.mixer.music.load('sounds/win_sound.mp3')
            pygame.mixer.music.play(0)
            show_win_message()
        if check_lose():
            pygame.mixer.music.load("sounds/lose_sound.mp3")
            pygame.mixer.music.play(0)
            show_lose_message()
        screen.blit(backgroud, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    terminate()