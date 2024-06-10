import pygame
import random

pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
snake = {
    "head": pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
    "body": [],
    "length": 1,
    "direction": pygame.Vector2(0, 10),
}

def randomly_position():
    return pygame.Vector2(
        random.randint(1, 72) * 10,
        random.randint(1, 72) * 10,
    )

def move(snake):
    snake['body'].append(snake['head'].copy())
    while len(snake['body']) > snake['length']:
        snake['body'].pop(0)
        
    snake['head'].y += snake['direction'].y
    snake['head'].x += snake['direction'].x

    snake['head'].y %= 720
    snake['head'].x %= 720

def control(snake):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if snake['direction'].x != 0:
            snake['direction'].x = 0
            snake['direction'].y = -10
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if snake['direction'].x != 0:
            snake['direction'].x = 0
            snake['direction'].y = 10
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if snake['direction'].y != 0:
            snake['direction'].x = -10
            snake['direction'].y = 0
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if snake['direction'].y != 0:
            snake['direction'].x = 10
            snake['direction'].y = 0

def draw (snake, ball, show_end_screen):
    # draw snake
    for element in snake['body']:
        pygame.draw.circle(screen, "purple", element, 4)
    pygame.draw.circle(screen, "green", snake['head'], 5)

    # draw ball
    pygame.draw.circle(screen, "red", ball, 5)

    if show_end_screen:
        # draw end screen
        pygame.draw.rect(screen, (0, 0, 0), (90, 110, 520, 520))
        pygame.draw.rect(screen, (100, 100, 100), (100, 100, 520, 520))

        font = pygame.font.Font('font.ttf', 32)
        smaller_font = pygame.font.Font('font.ttf', 16)

        text = font.render('Game Over', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (360, 340)
        screen.blit(text, textRect)

        smaller_text = smaller_font.render('Press \'r\' to restart.', True, (0, 0, 0))
        smaller_textRect = smaller_text.get_rect()
        smaller_textRect.center = (360, 370)
        screen.blit(smaller_text, smaller_textRect)

        even_smaller_text = smaller_font.render(f'Score: {snake["length"] - 1}', True, (0, 0, 0))
        even_smaller_textRect = even_smaller_text.get_rect()
        even_smaller_textRect.center = (360, 390)
        screen.blit(even_smaller_text, even_smaller_textRect)

def collided(head, objects):
    for obj in objects:
        if head.x == obj.x and head.y == obj.y:
            return True

    return False

if __name__ == "__main__":
    ball = randomly_position()
    running = True
    show_end_screen = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("gray")
        if not show_end_screen:
            control(snake)
            move(snake)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                snake = {
                    "head": pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
                    "body": [],
                    "length": 1,
                    "direction": pygame.Vector2(0, 10),
                }
                ball = randomly_position()
                show_end_screen = False

        if collided(snake['head'], [ball]):
            ball = randomly_position()
            snake['length'] += 1

        if collided(snake['head'], snake['body']):
            show_end_screen = True

        draw(snake, ball, show_end_screen)
        pygame.display.flip()
        clock.tick(20)

    pygame.quit()
