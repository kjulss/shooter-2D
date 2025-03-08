import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter 2D")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Jugador (nave espacial)
player_size = (50, 50)
player = pygame.Rect(WIDTH // 2, HEIGHT - 70, *player_size)
player_speed = 5

# Balas
bullets = []
bullet_speed = -7

# Enemigos
enemies = []
enemy_size = (50, 50)
enemy_speed = 2
spawn_timer = 30  # Tiempo entre la aparición de enemigos

# Fuente para la puntuación
font = pygame.font.Font(None, 36)
score = 0

# Cargar imágenes
player_img = pygame.image.load("player_ship.png")
player_img = pygame.transform.scale(player_img, player_size)
bullet_img = pygame.image.load("laser.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
enemy_img = pygame.image.load("enemy_ship.png")
enemy_img = pygame.transform.scale(enemy_img, enemy_size)

# Reloj para controlar FPS
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BLACK)
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.x + player.width // 2 - 5, player.y, 10, 20))
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
    
    # Mover balas
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)
    
    # Generar enemigos
    if spawn_timer <= 0:
        enemies.append(pygame.Rect(random.randint(0, WIDTH - enemy_size[0]), 0, *enemy_size))
        spawn_timer = 30
    spawn_timer -= 1
    
    # Mover enemigos
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
        
    # Colisiones entre balas y enemigos
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break
    
    # Dibujar jugador (nave), balas y enemigos
    screen.blit(player_img, (player.x, player.y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))
    
    # Mostrar puntuación
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
