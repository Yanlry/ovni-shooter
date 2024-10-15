import pygame
import random  
import time

pygame.init()

LARGEUR, HAUTEUR = 800, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Space Battle Shooter")

background = pygame.image.load('background_space.png')
background = pygame.transform.scale(background, (LARGEUR, HAUTEUR))
player_image = pygame.image.load('vaisseau_joueur.png')
player_image = pygame.transform.scale(player_image, (60, 60))
enemy_image = pygame.image.load('vaisseau_ennemi.png')
enemy_image = pygame.transform.scale(enemy_image, (80, 80))
ally_image = pygame.image.load('rocket.png')
ally_image = pygame.transform.scale(ally_image, (80, 80))
projectile_image = pygame.image.load('laser.png')
projectile_image = pygame.transform.scale(projectile_image, (10, 40))
super_pouvoir_image = pygame.image.load('super_pouvoir.png')
super_pouvoir_image = pygame.transform.scale(super_pouvoir_image, (40, 40))

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
VIOLET = (128, 0, 128)

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR // 2, HAUTEUR // 2)
        self.peut_rafale = False
        self.peut_tir_continu = False
        self.temps_debut_rafale = 0
        self.temps_debut_tir_continu = 0

    def update(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            self.rect.x -= 5
        if touches[pygame.K_RIGHT]:
            self.rect.x += 5
        if touches[pygame.K_UP]:
            self.rect.y -= 5
        if touches[pygame.K_DOWN]:
            self.rect.y += 5

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR:
            self.rect.right = LARGEUR
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HAUTEUR:
            self.rect.bottom = HAUTEUR

        if self.peut_rafale and time.time() - self.temps_debut_rafale > 4:
            self.peut_rafale = False

        if self.peut_tir_continu and time.time() - self.temps_debut_tir_continu > 4:
            self.peut_tir_continu = False

    def activer_rafale(self):
        self.peut_rafale = True
        self.temps_debut_rafale = time.time()

    def activer_tir_continu(self):
        self.peut_tir_continu = True
        self.temps_debut_tir_continu = time.time()

class Ennemi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        safe_zone = 100
        while True:
            self.rect.x = random.randint(0, LARGEUR - self.rect.width)
            self.rect.y = random.randint(0, HAUTEUR - self.rect.height)
            if abs(self.rect.x - joueur.rect.x) > safe_zone and abs(self.rect.y - joueur.rect.y) > safe_zone:
                break

    def update(self):
        self.rect.x += random.choice([-3, -2, -1, 1, 2, 3])
        self.rect.y += random.choice([-3, -2, -1, 1, 2, 3])

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > LARGEUR - self.rect.width:
            self.rect.x = LARGEUR - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HAUTEUR - self.rect.height:
            self.rect.y = HAUTEUR - self.rect.height

class Allie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ally_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGEUR - self.rect.width)
        self.rect.y = random.randint(0, HAUTEUR - self.rect.height)

    def update(self):
        self.rect.y += 3
        if self.rect.y > HAUTEUR:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = projectile_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        if self.direction == 'haut':
            self.rect.y -= 7
        elif self.direction == 'bas':
            self.rect.y += 7
        elif self.direction == 'gauche':
            self.rect.x -= 7
        elif self.direction == 'droite':
            self.rect.x += 7
        if self.rect.bottom < 0 or self.rect.top > HAUTEUR or self.rect.right < 0 or self.rect.left > LARGEUR:
            self.kill()

class Pouvoir(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = super_pouvoir_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGEUR - self.rect.width)
        self.rect.y = random.randint(0, HAUTEUR - self.rect.height)

    def update(self):
        pass

tous_les_sprites = pygame.sprite.Group()
ennemis = pygame.sprite.Group()
allies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
pouvoirs = pygame.sprite.Group()

joueur = Joueur()
tous_les_sprites.add(joueur)

niveau = 1
points = 0
ennemis_tues = 0

def restart_game():
    global joueur, tous_les_sprites, ennemis, allies, projectiles, pouvoirs, points
    tous_les_sprites.empty()
    ennemis.empty()
    allies.empty()
    projectiles.empty()
    pouvoirs.empty()

    joueur = Joueur()
    tous_les_sprites.add(joueur)
    points = 0

jeu_en_cours = True
horloge = pygame.time.Clock()
game_over = False

while jeu_en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu_en_cours = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_SPACE:
                    if joueur.peut_rafale:
                        directions = ['haut', 'bas', 'gauche', 'droite']
                        for direction in directions:
                            projectile = Projectile(joueur.rect.centerx, joueur.rect.centery, direction)
                            tous_les_sprites.add(projectile)
                            projectiles.add(projectile)
                    elif joueur.peut_tir_continu:
                        joueur.temps_debut_tir_continu = time.time()  
                    else:
                        projectile = Projectile(joueur.rect.centerx, joueur.rect.top, 'haut')
                        tous_les_sprites.add(projectile)
                        projectiles.add(projectile)
            if event.key == pygame.K_r and game_over:
                restart_game()
                game_over = False

    if joueur.peut_tir_continu and not game_over:
        if time.time() - joueur.temps_debut_tir_continu <= 4:
            projectile = Projectile(joueur.rect.centerx, joueur.rect.top, 'haut')
            tous_les_sprites.add(projectile)
            projectiles.add(projectile)
        else:
            joueur.peut_tir_continu = False

    if not game_over and random.randint(1, 100) <= 2:
        ennemi = Ennemi()
        tous_les_sprites.add(ennemi)
        ennemis.add(ennemi)

    if not game_over and random.randint(1, 200) <= niveau:
        allie = Allie()
        tous_les_sprites.add(allie)
        allies.add(allie)

    if not game_over and random.randint(1, 1000) <= 3:
        pouvoir = Pouvoir()
        tous_les_sprites.add(pouvoir)
        pouvoirs.add(pouvoir)

    if not game_over:
        tous_les_sprites.update()

    if not game_over:
        if pygame.sprite.spritecollide(joueur, ennemis, True):
            game_over = True

        if pygame.sprite.spritecollide(joueur, allies, True):
            game_over = True

        collisions = pygame.sprite.groupcollide(projectiles, ennemis, True, True)
        points += len(collisions)

        pouvoirs_collisions = pygame.sprite.spritecollide(joueur, pouvoirs, True)
        for pouvoir in pouvoirs_collisions:
            if random.choice([True, False]): 
                joueur.activer_rafale()
            else:
                joueur.activer_tir_continu()

    # 21 Affichage
    fenetre.blit(background, (0, 0))  
    tous_les_sprites.draw(fenetre) 

    font = pygame.font.SysFont(None, 36)
    texte_ennemis_tues = font.render(f'Ennemis tués: {points}', True, BLANC)
    fenetre.blit(texte_ennemis_tues, (LARGEUR - 200, 10))

    if game_over:
        game_over_font = pygame.font.SysFont(None, 50)
        game_over_text = game_over_font.render("Game Over! Appuyez sur 'R' pour redémarrer.", True, ROUGE)
        fenetre.blit(game_over_text, (LARGEUR // 2 - game_over_text.get_width() // 2, HAUTEUR // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()

    horloge.tick(60)

    if not game_over:
        pouvoirs_collisions = pygame.sprite.spritecollide(joueur, pouvoirs, True)
        for pouvoir in pouvoirs_collisions:
            if random.choice([True, False]): 
                joueur.activer_rafale()
            else:
                joueur.activer_tir_continu()

fenetre.blit(background, (0, 0)) 
tous_les_sprites.draw(fenetre)  

font = pygame.font.SysFont(None, 36)
texte_ennemis_tues = font.render(f'Ennemis tués: {points}', True, BLANC)
fenetre.blit(texte_ennemis_tues, (LARGEUR - 200, 10))

if game_over:
    game_over_font = pygame.font.SysFont(None, 50)
    game_over_text = game_over_font.render("Game Over! Appuyez sur 'R' pour redémarrer.", True, ROUGE)
    fenetre.blit(game_over_text, (LARGEUR // 2 - game_over_text.get_width() // 2, HAUTEUR // 2 - game_over_text.get_height() // 2))

pygame.display.flip()
