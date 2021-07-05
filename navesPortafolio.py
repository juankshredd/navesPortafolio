import pygame, random
#from os import system
#system("cls")
from pygame.constants import K_DOWN, K_RIGHT, K_UP
from os import system
system('cls')

WIDTH= 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (10,255,20)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JuegoNaves_Portfolio_JK")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
    BAR_LEN = 100
    BAR_HEI = 10
    fill = (percentage/100)* BAR_LEN
    border = pygame.Rect(x,y, BAR_LEN, BAR_HEI)
    fill = pygame.Rect(x,y, fill, BAR_HEI)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[K_RIGHT]:
            self.speed_x = 5
        if keystate[K_UP]:
            self.speed_y = -5
        if keystate[K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT-100:
            self.rect.y = HEIGHT-100
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # velocidad de explosion

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    draw_text(screen, "NAVES 2D JK", 65, WIDTH//2, HEIGHT//4)
    draw_text(screen, "Salvando al mundo de los asteroides", 27, WIDTH//2, HEIGHT//2)
    draw_text(screen, "Creado por: Juan Bohorquez", 27, WIDTH//2, HEIGHT//2 + 50)
    draw_text(screen, "Portfolio The Jabalí Company",27, WIDTH//2, HEIGHT//2 + 80)
    draw_text(screen, "Pulsa una tecla", 20, WIDTH//2, HEIGHT*0.75)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png",
"assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png", 
"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png",
"assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png", "assets/naveEnemy.png", "assets/naveEnemy1.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())


##-------------------Imagenes de explosion---------------

explosion_anim = []
for i in range (9):
    file = f"assets/regularExplosion0{i}.png"
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH+40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)


#cargar background
background = pygame.image.load("assets/background.png").convert()

#cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion2.mp3")
pygame.mixer.music.load("assets/musicaAccion.mp3")
pygame.mixer.music.set_volume(0.2)


pygame.mixer.music.play(loops=-1)

##-----GAME OVER -------##

game_over= True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0


    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    all_sprites.update()
    #colisiiones meteoro laser
    
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)

    for hit in hits:
        score += 1  
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor ) 

    #revisar colisiones jugador meteoro
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 20
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor ) 
        if player.shield <= 0:
            game_over = True

    screen.blit(background, [0,0])

    all_sprites.draw(screen)

    #marcador
    draw_text(screen,str(score), 25, WIDTH//2, 10 )

    #escudo
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()
pygame.quit()
