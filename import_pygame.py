import pygame
from sys import exit
from random import randint
import os


pepega=os.getcwd()

#choice([x,y,y,y])
class Zalud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        zalud_walk1 = pygame.image.load(str(pepega)+"/assets/zalud1.png").convert_alpha()
        zalud_walk2 = pygame.image.load(str(pepega)+"/assets/zalud2.png").convert_alpha()
        self.zalud_walk = [zalud_walk1, zalud_walk2]
        self.zalud_index = 0
        self.zalud_jump = pygame.image.load(str(pepega)+"/assets/zalud_jump.png").convert_alpha()
        
        self.image = self.zalud_walk[self.zalud_index]
        self.rect = self.image.get_rect(midbottom = (60, 490))
        self.gravity = 0
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 490:
            self.gravity = -20
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 490:
            self.rect.bottom = 490
    def animation(self):
        if self.rect.bottom < 490:
           self.image = self.zalud_jump
        else:    
           self.zalud_index += 0.1
           if self.zalud_index >= len(self.zalud_walk): 
               self.zalud_index = 0
           self.image = self.zalud_walk[int(self.zalud_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
       
        if type == "dollar": 
           self.image = pygame.image.load(str(pepega)+"/assets/dollar_p.png").convert_alpha()
           self.rect = self.image.get_rect(midbottom = (randint(1400,1600), 495))
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.rect.x -= 10
        self.destroy

def display_score():
    time = int(pygame.time.get_ticks() / 100) - start_time
    score_surface = score_font.render("Score: " + str(time), None, "White")  #f"{time}" může být místo str(time)
    score_rectangle = score_surface.get_rect(topleft = (20, 20)) 
    pygame.draw.rect(screen, "#ffd373", score_rectangle,0 , 10)
    pygame.draw.rect(screen, "#ffd373", score_rectangle, 20, 10)
    screen.blit(score_surface, score_rectangle)
    return time   

def collision_sprite():
   if pygame.sprite.spritecollide(player.sprite,enemy_group, False): 
       enemy_group.empty()
       die_sound.play()
       return False 
   else: 
       return True
        
#WINDOW
pygame.init()
screen = pygame.display.set_mode((1280, 720)) #screen
pygame.display.set_caption("ŽaludJump") #nazev okna
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0

die_sound = pygame.mixer.Sound(str(pepega)+"/assets/die.mp3")
bg_music = pygame.mixer.Sound(str(pepega)+"/assets/bg_music.mp3")
bg_music.set_volume(0.02)
bg_music.play(loops = -1)

player = pygame.sprite.GroupSingle()
player.add(Zalud())

enemy_group = pygame.sprite.Group()

background_surface = pygame.image.load(str(pepega)+"/assets/background.png").convert_alpha()

sky_surface = pygame.image.load(str(pepega)+"/assets/sky.png").convert() #vložení surface
sky_surface2 = pygame.image.load(str(pepega)+"/assets/sky.png").convert()

shadow_surface = pygame.image.load(str(pepega)+"/assets/shadow.png").convert_alpha()
ground_surface = pygame.image.load(str(pepega)+"/assets/ground.png").convert()
ground_surface2 = pygame.image.load(str(pepega)+"/assets/ground.png").convert()

text_font = pygame.font.Font(str(pepega)+"/assets/Pixellari.ttf",75)
text_surface = text_font.render("Žalud Jump", None, "White")
text_surface_outline = text_font.render("Žalud Jump", None, "#1f1f1f")

score_font = pygame.font.Font(str(pepega)+"/assets/Pixellari.ttf",50)

text_press_space = score_font.render("Press SPACE To start again",None,"White")
text_press_space_outline = score_font.render("Press SPACE To start again",None,"#1f1f1f")
text_press_space_rectangle = text_press_space.get_rect(center = (638, 650))
text_press_space_outline_rectangle = text_press_space_outline.get_rect(center = (635,650))

created_by_font = pygame.font.Font(str(pepega)+"/assets/Pixellari.ttf",30)
created_by = created_by_font.render("Created by Jakub \"Wajfy\" Kristl", None,"white")
created_by_rec = created_by.get_rect(bottomleft = (50, 550))
created_by_outline = created_by_font.render("Created by Jakub \"Wajfy\" Kristl", None,"#1f1f1f")
created_by_outline_rec = created_by_outline.get_rect(bottomleft = (47, 550))

dollar_x = randint(1400,1600) #X souřadnice dollaru
dollar_y = 445 #Y souřadnice dollaru
dollar_angle = 0
dollar_angle_speed = 10

dollar_surface = pygame.image.load(str(pepega)+"/assets/dollar_p.png").convert_alpha()
dollar_surface_rectangle = dollar_surface.get_rect (center = (dollar_x, dollar_y))

obstacle_rect_list = []

zalud_shadow_surface = pygame.image.load(str(pepega)+"/assets/dollar_shadow.png").convert_alpha()
zalud_shadow_surface_rectangle = zalud_shadow_surface.get_rect(midbottom = (60, 555))

text_x = 460 #X souřadnice nápisu
text_y = 60 #Y souřadnice nápisu

text_animation_speed = 0.5

sky_x = 0
sky_y = 0
sky_x2 = 1280
sky_y2 = 0
sky_speed = 1

ground_x = 0
ground_y = 480
ground_x2 = 1270
ground_y2 = 480
ground_speed = 3

zalud_gravity = 0

hitbox = False

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 700)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           exit()
        if game_active:

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_h: 
                   if hitbox == True:
                      hitbox = False                      
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h: 
                   if hitbox == False:
                      hitbox = True   
        
        else:    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 100)        
        
        if event.type == obstacle_timer and game_active:
            enemy_group.add(Obstacle("dollar"))
 
    #updates
    #mapa
    if game_active:
        sky_x -= sky_speed
        sky_x2 -= sky_speed
        screen.blit(sky_surface2, (sky_x2, sky_y2))
        screen.blit(sky_surface, (sky_x,sky_y))
        if sky_x < -1280:
            sky_x = 1280

        if sky_x2 < -1280:
            sky_x2 = 1280 

        screen.blit(shadow_surface, (0,475))

        screen.blit(ground_surface2, (ground_x2, ground_y2))
        screen.blit(ground_surface, (ground_x, ground_y))
        ground_x -= ground_speed
        ground_x2 -= ground_speed
        if ground_x < -1280:
            ground_x = 1260

        if ground_x2 < -1280:
            ground_x2 = 1260   

        score = display_score()

        #text
        screen.blit(text_surface_outline, (text_x - 4, text_y))
        screen.blit(text_surface, (text_x, text_y)) 
        
        #animace textu
        if text_y == 40:
            nahore = True
        elif text_y == 60:
            nahore = False

        if nahore == True:
            text_y += text_animation_speed
        elif nahore == False:
            text_y -= text_animation_speed
        screen.blit(zalud_shadow_surface, zalud_shadow_surface_rectangle)
        player.draw(screen)
        player.update()

        #enemy
        enemy_group.draw(screen)
        enemy_group.update()

        game_active = collision_sprite()

    else:
        zalud_gravity = 0

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface, (0,480))
        screen.blit(background_surface,(0,0))
        screen.blit(text_surface, (text_x, text_y))
        screen.blit(text_surface_outline, (text_x - 4, text_y))
        if text_y == 40:
            nahore = True
        elif text_y == 60:
            nahore = False

        if nahore == True:
            text_y += text_animation_speed
        elif nahore == False:
            text_y -= text_animation_speed

        score_message = text_font.render("Your score: "+ str(score), None, "White")
        score_message_rectangle = score_message.get_rect(center = (640, 400))
        score_message_outline = text_font.render("Your score: "+ str(score), None, "#1f1f1f")
        score_message_outline_rectangle = score_message.get_rect(center = (637, 400))
       
        welcome_text = text_font.render("Welcome", None, "White")
        welcome_text_rectangle = welcome_text.get_rect(center = (640, 400))
        welcome_text_outline = text_font.render("Welcome", None, "#1f1f1f")
        welcome_text_rectangle_outline = welcome_text.get_rect(center = (637, 400))

        if score == 0:
           screen.blit(welcome_text, welcome_text_rectangle)
           screen.blit(welcome_text_outline, welcome_text_rectangle_outline)
        else:       
           screen.blit(score_message, score_message_rectangle)
           screen.blit(score_message_outline, score_message_outline_rectangle)

        screen.blit(text_press_space, text_press_space_rectangle)
        screen.blit(text_press_space_outline, text_press_space_outline_rectangle)     
        
        screen.blit(created_by, created_by_rec)
        screen.blit(created_by_outline, created_by_outline_rec)
    pygame.display.update()
    clock.tick(60) #fps
