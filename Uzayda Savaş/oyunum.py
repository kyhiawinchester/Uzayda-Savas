import pygame
import sys
import random
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.init()

WIDTH, HEIGHT= 1280,720
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Uzayda Savaş")

BLACK=(0,0,0)

GREEN=(0,255,0)

RED=(255,0,0)

BLUE=(0,0,255)

WHITE=(255,255,255)

clock=pygame.time.Clock()
FPS=60

player_width=50
player_height=50
player_x=WIDTH//2-player_width//2
player_y=HEIGHT-player_height - 10
player_speed=10
player_skin="ship1"

bullet_width=5
bullet_height=10
bullet_speed=7
bullets=[]

enemy_width, enemy_height, enemy_speed = 50, 40, 3
enemies = []
enemy_types = [
    {"color": BLUE, "damage": 1},
    {"color": GREEN, "damage": 2}
]

items = [] 
item_width, item_height = 30, 30
item_speed = 2


in_main_menu=True
paused=False
in_skin_menu=False

#Skinler
skins=["ship1","ship2"]
skin_images={"ship1":pygame.image.load(resource_path("mor mutant.png")),"ship2":pygame.image.load(resource_path("Ezerim.png"))}
ship_image=skin_images[player_skin]
ship_width=ship_image.get_width()
ship_height=ship_image.get_height()

laser_image=pygame.image.load(resource_path("ateş.png"))

lives=3
score=0
font=pygame.font.SysFont(None,36)

pygame.mixer.init()

enemy_hit_sound = pygame.mixer.Sound(resource_path("enemy_hit.wav"))
game_over_sound = pygame.mixer.Sound(resource_path("game_over.wav"))
life_lost_sound = pygame.mixer.Sound(resource_path("life_lost.wav"))

def create_item():
    x = random.randint(0, WIDTH - item_width)
    y = random.randint(-100, -40)
    items.append([x, y])

def create_enemy():
    enemy_type = random.choice(enemy_types)
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-100, -40)
    enemies.append([x, y, enemy_type])

def display_score():
    score_text=font.render(f"Skor:{score}",True,WHITE)
    lives_text=font.render(f"Can:{lives}",True,WHITE)
    screen.blit(lives_text,(150,10))
    screen.blit(score_text,(10,10))

def game_over_screen():
    game_over_text=font.render("ÖLDÜN, YENİDEN BAŞLAMAK İÇİN 'R' YE BAS",True,WHITE)
    screen.blit(game_over_text,(WIDTH// 4, HEIGHT// 2))

def show_main_menu():
    menu_text=font.render("Uzayda Savaş-Başlamak İçin BOŞLUK'A TIKLA",True,WHITE)
    screen.blit(menu_text,(WIDTH//6,HEIGHT//2-20))

def show_pause_screen():
    pause_text=font.render("Oyun Duraklatıldı-Devam için ESC",True,WHITE)
    screen.blit(pause_text,(WIDTH//6,HEIGHT//2))

def show_skin_menu():
    skin_text=font.render("Gemi Seç",True,WHITE)
    screen.blit(skin_text,(WIDTH//3, HEIGHT//2-100))

    for i, skin in enumerate(skins):
        screen.blit(skin_images[skin],(WIDTH//4+i*150,HEIGHT//2))

#Oyun Döngüsü
running=True
game_over=False

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    if in_main_menu:
        show_main_menu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE:
                in_main_menu=False
                in_skin_menu=True
        continue
    
    if in_skin_menu:
        show_skin_menu()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    current_skin_index=skins.index(player_skin)
                    player_skin=skins[(current_skin_index+1)%len(skins)]
                elif event.key==pygame.K_LEFT:
                    current_skin_index=skins.index(player_skin)
                    player_skin=skins[(current_skin_index-1)%len(skins)]
                elif event.key==pygame.K_RETURN:
                    in_skin_menu=False
        continue

    if paused:
        show_pause_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused=False
        continue

    if random.randint(1, 300) == 1: 
     create_item()

     for enemy in enemies:
      pygame.draw.rect(screen, enemy[2]["color"], (enemy[0], enemy[1], enemy_width, enemy_height))
     
    for item in items:
     item[1] += item_speed

     items = [i for i in items if i[1] < HEIGHT]


     for item in items:
      pygame.draw.rect(screen, RED, (item[0], item[1], item_width, item_height))
   
        
    if game_over:
        game_over_screen()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_r:
                   score=0
                   enemies.clear()
                   items.clear()
                   bullets.clear()
                   player_x=WIDTH//2-player_width//2
                   player_y=HEIGHT-player_height-10
                   enemy_speed=3
                   lives=3
                   game_over=False
        continue           
    
    #OLAYLAR
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        #Mermi Ateşle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_ship_image=skin_images[player_skin]
                ship_width=current_ship_image.get_width()
                bullet_x=player_x+ship_width//2-bullet_width//2
                bullet_y=player_y
                bullets.append([bullet_x,bullet_y])
            if event.key == pygame.K_ESCAPE:
                paused=True

    #Tuşlarla Hareket
    keys=pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x >0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < WIDTH-player_width:
        player_x += player_speed
    if keys[pygame.K_w] and player_y >0:
        player_y -= player_speed
    if keys[pygame.K_s] and player_y < HEIGHT - player_height:
        player_y += player_speed

    #Düşmanları Hareket ettir
    for enemy in enemies:
        enemy[1] +=enemy_speed

    #Ekran Dışına Çıkan Düşmanları Sil
    enemies=[enemy for enemy in enemies if enemy[1] < HEIGHT]
    
    #Çarpışma Kontrolu
    player_rect = pygame.Rect(player_x, player_y, ship_width, ship_height)

    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            if bullet_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                enemy_hit_sound.play()
                break

            
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            lives -= enemy[2]["damage"]
            enemies.remove(enemy)
            if lives > 0:
                life_lost_sound.play()
            else:
                game_over_sound.play()
                game_over = True
            break
                     
    #Yeni Düşman Ekle
    if random.randint(1,60)==1:
     create_enemy()
    
     
     player_rect = pygame.Rect(player_x, player_y, ship_width, ship_height) 
     for item in items[:]:
      item_rect = pygame.Rect(item[0], item[1], item_width, item_height)
      if player_rect.colliderect(item_rect):
        lives += 1
        items.remove(item)

    #Skor Arttıkça Düşman Hızlansın
    if score > 10:
        enemy_speed=4
    if score > 20:
        enemy_speed=5
    if score > 30:
        enemy_speed=6
    
    #Mermileri Hareket ettir
    for bullet in bullets:
        bullet[1] -=bullet_speed

    #Ekran dışına çıkan mermileri sil
    bullets = [b for b in bullets if b[1]>0]

    #Skin ile gemi çizme
    screen.blit(skin_images[player_skin],(player_x,player_y))
    
    #Düşmanları Çiz
    screen.blit(skin_images[player_skin], (player_x, player_y))

    for enemy in enemies:
        pygame.draw.rect(screen, enemy[2]["color"], (enemy[0], enemy[1], enemy_width, enemy_height))
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, (bullet[0], bullet[1], 4, 20))
    for item in items:
        pygame.draw.rect(screen, RED, (item[0], item[1], item_width, item_height))

    #Mermileri Çiz
    for bullet in bullets:
        pygame.draw.rect(screen,(0,255,255),(bullet[0],bullet[1],4,20))
    #Skoru Ekrana yazdır
    display_score()

    pygame.display.flip()                   

#ÇIKIŞ
pygame.quit()
sys.exit