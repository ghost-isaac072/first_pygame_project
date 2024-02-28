import os
import random
import sys
import pygame
pygame.init()

TILE_SIZE = 32
SCREEN_INFO = pygame.display.Info()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = SCREEN_INFO.current_w, SCREEN_INFO.current_h
MAPS_DIR = "maps"
FPS = 60
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
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
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    background = pygame.transform.scale(load_image('start_screen.jpg'), (800, 600))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


class Ball(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("ball.png"), (TILE_SIZE, TILE_SIZE))
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.rect.


class Board:
    def __init__(self, filename):
        self.map = []
        with open(os.path.join(MAPS_DIR, filename)) as input_file:
            for line in input_file:
                self.map.append((list(map(int, line.split()))))
        self.tile_size = TILE_SIZE
        self.height = len(self.map)

    def render(self):
        for y in range(self.height):
            for x in range(len(self.map[y])):
                if self.get_tile_id((x, y)):
                    ball = Ball(x * TILE_SIZE, y * TILE_SIZE)
                    all_sprites.add(ball)
                    all_balls.add(ball)


                #rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
               #                    self.tile_size, self.tile_size)
               # screen.fill(colors[self.get_tile_id((x, y))], rect)
    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.x = WINDOW_WIDTH // 2 - 50
        self.y = WINDOW_HEIGHT - 100
        self.image = pygame.Surface([200, 20], pygame.SRCALPHA, 32)
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)

    def update(self):
        self.rect.center = (pygame.mouse.get_pos()[0], WINDOW_HEIGHT - 50)

class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('player.png'), (50, 50))
    def __init__(self):
        super().__init__(all_sprites)
        self.x = WINDOW_WIDTH // 2 - 50
        self.y = WINDOW_HEIGHT - 100
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30 - self.rect.height)
        self.vx = 5 * random.choice([1, -1])
        self.vy = -5

    def update(self):
        if not moving:
            self.rect.center = (pygame.mouse.get_pos()[0], WINDOW_HEIGHT - 30 - self.rect.height)
        else:
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, platform):
                self.vy = -self.vy
            hits = pygame.sprite.spritecollide(self, all_balls, True)
            if hits:
                print(hits[0].rect.x)



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
    #screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Арканоид на pygame ver 1.0.')
    clock = pygame.time.Clock()

    #start_screen()

    all_sprites = pygame.sprite.Group()
    all_balls = pygame.sprite.Group()
    board = Board('map_1.txt')
    board.render()

    platform = Platform()
    player = Player()

    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()


    Border(1, 0, WINDOW_WIDTH, 0)
    Border(0, WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
    Border(0, 0, 0, WINDOW_HEIGHT)
    Border(WINDOW_WIDTH - 190, 0, WINDOW_WIDTH - 190, WINDOW_HEIGHT)

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
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    terminate()