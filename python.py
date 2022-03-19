from copyreg import constructor
import pygame
from sys import exit
from random import randint, choice


class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def click_input(self):
        if self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle (pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load(
                "graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load(
                "graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

def display_score():
    time = pygame.time.get_ticks() - start_time
    score_surf = score_font.render(
        f"Score: {int(time/1000)}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
score_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("audio/music.wav")

# Groups #
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Map surfaces #
sky_surf = pygame.image.load("graphics/sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()

# Menu surfaces #
game_title = score_font.render("Pixel Runner", False, (111, 196, 169))
game_title_rect = game_title.get_rect(center=(400, 50))

game_message = score_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 350))

# Player Menu surfaces #
player_stand = pygame.image.load(
    "graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timers #
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 100)

bg_music.play(loops = -1)


while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.sprite.click_input()

            if event.type == obstacle_timer:
                obstacle_group.add( Obstacle(choice(["fly", "snail"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    # Game
    if game_active:
        # Show Background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

    # Menu
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        game_score = score_font.render(f"Last Score: {int(score/1000)}", False, (111, 196, 169))
        game_score_rect = game_score.get_rect(center=(400, 350))
        screen.blit(game_title, game_title_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(game_score, game_score_rect)

    pygame.display.update()
    clock.tick(60)
