#John Dannrill Cruz
import pygame
import random
import math


pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
WINNING_SCORE = 5


font = pygame.font.Font(None, 36)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

#Lagera, Shayne
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 6
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        
#Jhon Mark Pahanonot   
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction_y *= -1

    def bounce_off_paddle(self, paddle):
        self.direction_x *= -1
        self.rect.x += self.speed * self.direction_x


       
        ball_center = self.rect.centery
        paddle_center = paddle.rect.centery
        relative_intersect_y = (paddle_center - ball_center) / (paddle.rect.height / 2)
        bounce_angle = relative_intersect_y * (math.pi / 4)
        self.direction_y = math.sin(bounce_angle)

# Score
score1 = 0
score2 = 0

def show_score():
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

#Rhick Charles Dela Cruz
paddle1 = Paddle(WHITE, 10, 100)
paddle1.rect.x = 30
paddle1.rect.y = HEIGHT // 2 - 50

paddle2 = Paddle(WHITE, 10, 100)
paddle2.rect.x = WIDTH - 40
paddle2.rect.y = HEIGHT // 2 - 50

ball = Ball(WHITE, 10, 10)
ball.rect.x = WIDTH // 2
ball.rect.y = HEIGHT // 2

all_sprites = pygame.sprite.Group()
all_sprites.add(paddle1, paddle2, ball)



STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
state = STATE_MENU


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == STATE_MENU or state == STATE_PAUSED:
                    state = STATE_PLAYING
                elif state == STATE_PLAYING:
                    state = STATE_PAUSED
                elif state == STATE_GAME_OVER:
                    state = STATE_MENU
                    score1 = 0
                    score2 = 0
                    ball.rect.x = WIDTH // 2
                    ball.rect.y = HEIGHT // 2
                    ball.direction_x = random.choice([-1, 1])
                    ball.direction_y = random.choice([-1, 1])

    if state == STATE_PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.rect.y -= 7
        if keys[pygame.K_s]:
            paddle1.rect.y += 7
        if keys[pygame.K_UP]:
            paddle2.rect.y -= 7
        if keys[pygame.K_DOWN]:
            paddle2.rect.y += 7

#Raizel Alyna Mae Centeno               
        ball.update()
        
        
        if pygame.sprite.collide_rect(ball, paddle1) or pygame.sprite.collide_rect(ball, paddle2):
            ball.bounce_off_paddle(paddle1) if pygame.sprite.collide_rect(ball, paddle1) else ball.bounce_off_paddle(paddle2)
        
        
        if ball.rect.x >= WIDTH:
            score1 += 1
            ball.rect.x = WIDTH // 2
            ball.rect.y = HEIGHT // 2
            ball.direction_x = random.choice([-1, 1])
            ball.direction_y = random.choice([-1, 1])
        
        if ball.rect.x <= 0:
            score2 += 1
            ball.rect.x = WIDTH // 2
            ball.rect.y = HEIGHT // 2
            ball.direction_x = random.choice([-1, 1])
            ball.direction_y = random.choice([-1, 1])

#Ronald Orpilla             
        if score1 >= WINNING_SCORE or score2 >= WINNING_SCORE:
            state = STATE_GAME_OVER
    
    
    screen.fill(BLACK)
    
    
    all_sprites.draw(screen)
    show_score()
    
    
    if state == STATE_MENU:
        start_button_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start_button_text, (WIDTH // 2 - start_button_text.get_width() // 2, HEIGHT // 2))
    elif state == STATE_PAUSED:
        paused_text = font.render("Paused", True, WHITE)
        screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2))
    elif state == STATE_GAME_OVER:
        winner_text = font.render(f"Game Over! {'Player 1' if score1 >= WINNING_SCORE else 'Player 2'} Wins!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    
    
    pygame.display.flip()
    
    
    clock.tick(FPS)


pygame.quit()