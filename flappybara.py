import pygame
import random
import sys

# Game settings
WIDTH, HEIGHT = 400, 600
GROUND_HEIGHT = 80
BIRD_SIZE = 30
PIPE_WIDTH = 60
GAP_SIZE = 150
GRAVITY = 0.5
JUMP_STRENGTH = -10
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x - BIRD_SIZE//2, self.y - BIRD_SIZE//2, BIRD_SIZE, BIRD_SIZE)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y - BIRD_SIZE//2
        if self.rect.bottom > HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self, surface):
        pygame.draw.ellipse(surface, (255, 200, 0), self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(50, HEIGHT - GROUND_HEIGHT - GAP_SIZE - 50)
        self.bottom_height = HEIGHT - GROUND_HEIGHT - self.top_height - GAP_SIZE
        self.passed = False

    def update(self):
        self.x -= 3

    def offscreen(self):
        return self.x + PIPE_WIDTH < 0

    def collide(self, bird_rect):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(self.x, HEIGHT - GROUND_HEIGHT - self.bottom_height, PIPE_WIDTH, self.bottom_height)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

    def draw(self, surface):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(self.x, HEIGHT - GROUND_HEIGHT - self.bottom_height, PIPE_WIDTH, self.bottom_height)
        pygame.draw.rect(surface, (0, 255, 0), top_rect)
        pygame.draw.rect(surface, (0, 255, 0), bottom_rect)


def draw_ground(surface):
    ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
    pygame.draw.rect(surface, (160, 82, 45), ground_rect)

def main():
    bird = Bird()
    pipes = []
    score = 0
    frame_count = 0
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_r and bird.rect.bottom >= HEIGHT - GROUND_HEIGHT:
                    return  # restart
        bird.update()
        if frame_count % 90 == 0:
            pipes.append(Pipe(WIDTH))
        for pipe in list(pipes):
            pipe.update()
            if pipe.offscreen():
                pipes.remove(pipe)
            if pipe.collide(bird.rect):
                running = False
            if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                score += 1
                pipe.passed = True
        screen.fill((135, 206, 235))
        for pipe in pipes:
            pipe.draw(screen)
        draw_ground(screen)
        bird.draw(screen)
        score_text = font.render(str(score), True, (0,0,0))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        pygame.display.flip()
        frame_count += 1
    # Game over
    msg = font.render('Game Over! Press R to Restart', True, (255,0,0))
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
    pygame.display.flip()
    # Wait for restart or quit
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

if __name__ == '__main__':
    while True:
        main()
