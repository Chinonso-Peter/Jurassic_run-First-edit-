import pygame
from sys import exit
from random import randint, choice
import os

PATH = os.path.abspath('.') + '/'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_run1 = pygame.image.load(PATH + "assets/Player/player_run1.png").convert_alpha()
        player_run2 = pygame.image.load(PATH + "assets/Player/player_run2.png").convert_alpha()
        player_run3 = pygame.image.load(PATH + "assets/Player/player_run3.png").convert_alpha()
        player_run4 = pygame.image.load(PATH + "assets/Player/player_run4.png").convert_alpha()
        player_run5 = pygame.image.load(PATH + "assets/Player/player_run5.png").convert_alpha()
        player_run6 = pygame.image.load(PATH + "assets/Player/player_run6.png").convert_alpha()
        self.player_run = [player_run1, player_run2, player_run3, player_run4, player_run5, player_run6]
        self.player_index = 0
        self.player_jump = pygame.image.load("assets/Player/player_run5.png").convert_alpha()

        self.image = self.player_run[self.player_index]
        self.rect = self.image.get_rect(center=(200, 310))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom == 410:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 410:
            self.rect.bottom = 410

    def animation_state(self):
        if self.rect.bottom < 410:
            self.image = self.player_jump
        else:
            self.player_index += 0.2
            if self.player_index >= len(self.player_run):
                self.player_index = 0
            self.image = self.player_run[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def create_bullet(self):
        return Bullet(self.rect.centerx + 95, self.rect.top + 53)

    def collide(self):
        self.rect.bottom = 410


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "cactus":
            cactus1 = pygame.image.load(PATH + "assets/Obstacle/cactus.png").convert_alpha()
            cactus2 = pygame.image.load(PATH + "assets/Obstacle/cactus.png").convert_alpha()
            self.frames = [cactus1, cactus2]
            y_pos = 400
        else:
            dino1 = pygame.image.load(PATH + "assets/Dino/dino_run1.png").convert_alpha()
            dino2 = pygame.image.load(PATH + "assets/Dino/dino_run2.png").convert_alpha()
            dino3 = pygame.image.load(PATH + "assets/Dino/dino_run3.png").convert_alpha()
            dino4 = pygame.image.load(PATH + "assets/Dino/dino_run4.png").convert_alpha()
            dino5 = pygame.image.load(PATH + "assets/Dino/dino_run5.png").convert_alpha()
            dino6 = pygame.image.load(PATH + "assets/Dino/dino_run6.png").convert_alpha()
            self.frames = [dino1, dino2, dino3, dino4, dino5, dino6]
            y_pos = 400

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1100, 1300), y_pos))

    def animation_state(self):
        self.animation_index += 0.15
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def destroy(self):
        if self.rect.left >= 1000:
            self.kill()

    def update(self):
        self.rect.x += 30
        self.destroy()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(PATH + "assets/graphics/cloud.png")
        self.rect = self.image.get_rect(midtop=(200, 1))

    def move(self):
        self.rect.x -= 5
        if self.rect.x <= -2000:
            self.rect.x = 1100

    def update(self):
        self.move()


def display_score():
    current_time = pygame.time.get_ticks() // 1000 - start_time
    score_surf = test_font.render(f"SCORE: {current_time}", False, (255, 0, 0))
    score_rect = score_surf.get_rect(center=(500, 50))
    screen.blit(score_surf, score_rect)
    return current_time


pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Jurassic Run")
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound(PATH + "assets/Sound/bgmusic.wav")
bg_music.play(-1)
gun_sound = pygame.mixer.Sound(PATH + "assets/Sound/gunsound.mp3")

# Background
sky_surface = pygame.image.load(PATH + "assets/graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load(PATH + "assets/graphics/ground.png").convert_alpha()
test_font = pygame.font.Font(None, 60)
game_name = test_font.render("Jurassic Run", False, (0, 0, 1))
game_name_rect = game_name.get_rect(center=(200, 250))
game_message = test_font.render("Click play to start", False, (0, 0, 1))
game_message_rect = game_message.get_rect(center=(500, 450))

# Groups
players = pygame.sprite.Group()
player = Player()
players.add(player)
bullets = pygame.sprite.Group()
clouds = pygame.sprite.Group()
cloud = Cloud()
clouds.add(cloud)
obstacles = pygame.sprite.Group()

# Buttons
jump_button = pygame.image.load(PATH + "assets/Buttons/jump.png").convert_alpha()
jump_button_rect = jump_button.get_rect(midbottom=(100, 490))

shoot_button = pygame.image.load(PATH + "assets/Buttons/shoot.png").convert_alpha()
shoot_button_rect = shoot_button.get_rect(midbottom=(850, 490))

# Menu Buttons
play_button = test_font.render("PLAY", False, (0, 0, 1))
play_button_rect = play_button.get_rect(center=(500, 150))

quit_button = test_font.render("QUIT", False, (0, 0, 1))
quit_button_rect = quit_button.get_rect(center=(500, 250))

enemy_live = 3

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.add(player.create_bullet())
                    # gun_sound.set_volume(1.0)
                    gun_sound.play()
                if event.key == pygame.K_UP and player.rect.bottom == 410:
                    player.gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if jump_button_rect.collidepoint(event.pos) and player.rect.bottom == 410:
                    player.gravity = -20
                if shoot_button_rect.collidepoint(event.pos):
                    bullets.add(player.create_bullet())
                    # gun_sound.set_volume(1)
                    gun_sound.play()
        else:
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #     game_active = True
            #     start_time = pygame.time.get_ticks() // 1000
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_active = True
                    start_time = pygame.time.get_ticks() // 1000
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(["cactus", "cactus", "dino ", "dino"])))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 400))
        players.draw(screen)
        bullets.draw(screen)
        clouds.draw(screen)
        obstacles.draw(screen)
        players.update()
        bullets.update()
        clouds.update()
        obstacles.update()
        score = display_score()
        # bg_music.set_volume(0.3)
        # bg_music.play(-1)

        # Buttons
        pygame.draw.rect(screen, (0, 255, 0), jump_button_rect)
        screen.blit(jump_button, jump_button_rect)
        pygame.draw.rect(screen, (255, 0, 0), shoot_button_rect)
        screen.blit(shoot_button, shoot_button_rect)

        # check if bullet hits the enemy
        hit = pygame.sprite.groupcollide(obstacles, bullets, True, True)

        # check if enemy hit player
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            game_active = False
            player.collide()
            obstacles.empty()

    else:
        screen.fill((0, 0, 1))

        score_message = test_font.render(f"Your Score: {score}", False, (0, 0, 1))
        score_message_rect = score_message.get_rect(center=(500, 80))
        screen.blit(game_name, game_name_rect)
        pygame.draw.rect(screen, "Green", play_button_rect)
        screen.blit(play_button, play_button_rect)
        pygame.draw.rect(screen, "Green", quit_button_rect)
        screen.blit(quit_button, quit_button_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
