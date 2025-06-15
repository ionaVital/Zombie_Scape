import pgzrun
from pygame import Rect
import random

WIDTH = 640
HEIGHT = 640
TITLE = "Zombie Scape"

TILE_SIZE = 64
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

hero_idle_images = ["hero_idle1", "hero_idle2"]
hero_walk_images = ["hero_walk1", "hero_walk2"]

enemy_idle_images = ["enemy_idle1", "enemy_idle2"]
enemy_walk_images = ["enemy_walk1", "enemy_walk2"]

sounds_enabled = True
music.set_volume(0.3)
music.play("mystery")

menu_active = True
game_over = False

menu_buttons = [
    Rect((220, 200, 200, 50)),
    Rect((220, 270, 200, 50)),
    Rect((220, 340, 200, 50))
]

class Entity:
    def __init__(self, grid_x, grid_y, idle_images, walk_images):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x = grid_x * TILE_SIZE
        self.pos_y = grid_y * TILE_SIZE
        self.idle_images = idle_images
        self.walk_images = walk_images
        self.image_index = 0
        self.frame_count = 0
        self.is_moving = False
        self.target_pos_x = self.pos_x
        self.target_pos_y = self.pos_y
        self.speed = 8

    def update(self):
        self._update_position()
        self._update_animation()

    def _update_position(self):
        if self.pos_x < self.target_pos_x:
            self.pos_x = min(self.pos_x + self.speed, self.target_pos_x)
            self.is_moving = True
        elif self.pos_x > self.target_pos_x:
            self.pos_x = max(self.pos_x - self.speed, self.target_pos_x)
            self.is_moving = True
        elif self.pos_y < self.target_pos_y:
            self.pos_y = min(self.pos_y + self.speed, self.target_pos_y)
            self.is_moving = True
        elif self.pos_y > self.target_pos_y:
            self.pos_y = max(self.pos_y - self.speed, self.target_pos_y)
            self.is_moving = True
        else:
            self.is_moving = False

        if not self.is_moving:
            self.grid_x = self.target_pos_x // TILE_SIZE
            self.grid_y = self.target_pos_y // TILE_SIZE

    def _update_animation(self):
        self.frame_count = (self.frame_count + 1) % 10
        if self.frame_count == 0:
            images = self.walk_images if self.is_moving else self.idle_images
            self.image_index = (self.image_index + 1) % len(images)

    def draw(self):
        images = self.walk_images if self.is_moving else self.idle_images
        current_image = images[self.image_index]
        screen.blit(current_image, (self.pos_x, self.pos_y))

class Hero(Entity):
    def move(self, dx, dy):
        if game_over or self.is_moving:
            return
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.target_pos_x = new_x * TILE_SIZE
            self.target_pos_y = new_y * TILE_SIZE
            if sounds_enabled:
                sounds.move.play()

class Enemy(Entity):
    def advance(self):
        if self.is_moving:
            return

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                self.target_pos_x = new_x * TILE_SIZE
                self.target_pos_y = new_y * TILE_SIZE
                break

hero = Hero(1, 1, hero_idle_images, hero_walk_images)
enemies = [
    Enemy(5, 5, enemy_idle_images, enemy_walk_images),
    Enemy(8, 2, enemy_idle_images, enemy_walk_images)
]

def update():
    global menu_active, game_over

    if menu_active or game_over:
        return

    hero.update()
    for enemy in enemies:
        enemy.update()
        if not enemy.is_moving:
            enemy.advance()

    check_collision()

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
    screen.draw.text("Zombie Scape", center=(WIDTH // 2, 100), fontsize=48, color="white")
    labels = ["COMECAR",
              "Musica: ON" if sounds_enabled else "Musica: OFF",
              "SAIR"]
    for rect, label in zip(menu_buttons, labels):
        screen.draw.filled_rect(rect, "green")
        screen.draw.textbox(label, rect, color="white")

def draw_game_over():
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
    screen.draw.text("Pressione ENTER para retornar ao menu", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=32, color="white")

def check_collision():
    global game_over
    for enemy in enemies:
        if hero.grid_x == enemy.grid_x and hero.grid_y == enemy.grid_y:
            game_over = True
            if sounds_enabled:
                sounds.game_over.play()
            music.stop()

def on_key_down(key):
    global menu_active, game_over

    if menu_active:
        return

    if game_over:
        if key == keys.RETURN:
            reset_game()
            menu_active = True
    else:
        if key == keys.LEFT:
            hero.move(-1, 0)
        elif key == keys.RIGHT:
            hero.move(1, 0)
        elif key == keys.UP:
            hero.move(0, -1)
        elif key == keys.DOWN:
            hero.move(0, 1)

def reset_game():
    global hero, enemies, game_over
    hero = Hero(1, 1, hero_idle_images, hero_walk_images)
    enemies.clear()
    enemies.extend([
        Enemy(5, 5, enemy_idle_images, enemy_walk_images),
        Enemy(8, 2, enemy_idle_images, enemy_walk_images)
    ])
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
