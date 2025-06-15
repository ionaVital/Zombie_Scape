import pgzrun
import random
from pygame import Rect

WIDTH = 640
HEIGHT = 640
TITLE = "Zombie Scape"

TILE_SIZE = 64
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

hero_images = ["hero_idle1", "hero_idle2"]
hero_walk_images = ["hero_walk1", "hero_walk2"]

enemy_images = ["enemy_idle1", "enemy_idle2"]
enemy_walk_images = ["enemy_walk1", "enemy_walk2"]

sounds_enabled = True
music.play("mystery")
music.set_volume(0.3)

menu_active = True
game_over = False
menu_buttons = [
    Rect((220, 200, 200, 50)),
    Rect((220, 270, 200, 50)), 
    Rect((220, 340, 200, 50))   
]

class Entity:
    def __init__(self, x, y, images_idle, images_walk):
        self.x = x
        self.y = y
        self.images_idle = images_idle
        self.images_walk = images_walk
        self.image_index = 0
        self.frame = 0
        self.target = (x, y)
        self.is_moving = False

    def screen_pos(self):
        return self.x * TILE_SIZE, self.y * TILE_SIZE

    def update_position(self):
        tx, ty = self.target
        self.is_moving = False
        if self.x < tx:
            self.x += 1
            self.is_moving = True
        elif self.x > tx:
            self.x -= 1
            self.is_moving = True
        elif self.y < ty:
            self.y += 1
            self.is_moving = True
        elif self.y > ty:
            self.y -= 1
            self.is_moving = True

    def update_animation(self):
        self.frame = (self.frame + 1) % 15
        if self.frame == 0:
            self.image_index = (self.image_index + 1) % len(self.images_idle)

    def draw(self):
        images = self.images_walk if self.is_moving else self.images_idle
        img = images[self.image_index]
        screen.blit(img, self.screen_pos())

class Hero(Entity):
    def move(self, dx, dy):
        if game_over:
            return
        tx, ty = self.x + dx, self.y + dy
        if 0 <= tx < GRID_WIDTH and 0 <= ty < GRID_HEIGHT:
            self.x, self.y = tx, ty
            self.is_moving = True
            if sounds_enabled:
                sounds.move.play()
            for enemy in enemies:
                enemy.advance()
            check_collision()

class Enemy(Entity):
    def __init__(self, x, y, images_idle, images_walk, patrol_points):
        super().__init__(x, y, images_idle, images_walk)
        self.patrol_points = patrol_points
        self.current_target = 1

    def advance(self):
        self.is_moving = False
        tx, ty = self.patrol_points[self.current_target]
        if self.x < tx:
            self.x += 1
            self.is_moving = True
        elif self.x > tx:
            self.x -= 1
        elif self.y < ty:
            self.y += 1
        elif self.y > ty:
            self.y -= 1
        else:
            self.current_target = (self.current_target + 1) % len(self.patrol_points)


hero = Hero(1, 1, hero_images, hero_walk_images)
enemies = [
    Enemy(5, 5, enemy_images, enemy_walk_images, [(5, 5), (7, 5)]),
    Enemy(8, 2, enemy_images, enemy_walk_images, [(8, 2), (8, 4)])
]


def update():
    if not menu_active and not game_over:
        hero.is_moving = False
        hero.update_animation()
        for enemy in enemies:
            enemy.is_moving = False
            enemy.update_animation()

def draw():
    screen.clear()
    if menu_active:
        draw_menu()
    elif game_over:
        draw_game_over()
    else:
        draw_grid()
        hero.draw()
        for enemy in enemies:
            enemy.draw()

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            screen.blit("tile_floor", (x * TILE_SIZE, y * TILE_SIZE))

def draw_menu():
    screen.draw.text("Zombie Scape", center=(WIDTH//2, 100), fontsize=48, color="white")
    labels = ["COMECAR", "Musica", "Sair"]
    for rect, label in zip(menu_buttons, labels):
        screen.draw.filled_rect(rect, "green")
        screen.draw.textbox(label, rect, color="white")
        
def draw_game_over():
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
    screen.draw.text("Pressione ENTER para retornar ao menu", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=32, color="white")

def check_collision():
    global game_over
    for enemy in enemies:
        if hero.x == enemy.x and hero.y == enemy.y:
            game_over = True
            if sounds_enabled:
                sounds.game_over.play()
            music.stop()

def on_key_down(key):
    global menu_active, game_over
    if not menu_active and not game_over:
        if key == keys.LEFT:
            hero.move(-1, 0)
        elif key == keys.RIGHT:
            hero.move(1, 0)
        elif key == keys.UP:
            hero.move(0, -1)
        elif key == keys.DOWN:
            hero.move(0, 1)
    elif game_over and key == keys.RETURN:
        reset_game()
        menu_active = True

def reset_game():
    global hero, enemies, game_over
    hero = Hero(1, 1, hero_images, hero_walk_images)
    enemies = [
        Enemy(5, 5, enemy_images, enemy_walk_images, [(5, 5), (7, 5)]),
        Enemy(8, 2, enemy_images, enemy_walk_images, [(8, 2), (8, 4)])
    ]
    game_over = False
    if sounds_enabled:
        music.play("mystery")

def on_mouse_down(pos):
    global menu_active, sounds_enabled
    if menu_active:
        if menu_buttons[0].collidepoint(pos):
            menu_active = False
        elif menu_buttons[1].collidepoint(pos):
            sounds_enabled = not sounds_enabled
            if sounds_enabled:
                music.play("mystery")
            else:
                music.stop()
        elif menu_buttons[2].collidepoint(pos):
            exit()

pgzrun.go()