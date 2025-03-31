import pygame
import random
import sys

pygame.init()

# Размеры экрана и клетки
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

# Настройка экрана и шрифта
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake_Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Начальные параметры змейки
snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)
score = 0
level = 1
speed = 10

# Стены по краям поля
walls = []
for x in range(COLS):

    walls.append((x, 0))

    walls.append((x, ROWS - 1))

for y in range(ROWS):

    walls.append((0, y))

    walls.append((COLS - 1, y))

# Параметры еды
food = None  # позиция еды
food_weight = 1  # вес еды
food_timer = 0   # таймер для удаления еды
FOOD_LIFESPAN = 300  # количество кадров до исчезновения (примерно 30 секунд при 10 fps)

# Функция для генерации еды
def get_food_position():

    while True:

        x = random.randint(1, COLS - 2)

        y = random.randint(1, ROWS - 2)

        if (x, y) not in snake and (x, y) not in walls:

            return (x, y)

# Отрисовка всех игровых элементов
def draw_game(food_pos):

    screen.fill(BLACK)

    # Рисуем стены
    for wall in walls:

        pygame.draw.rect(screen, GRAY, (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Рисуем змейку
    for segment in snake:

        pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Рисуем еду
    pygame.draw.rect(screen, RED, (food_pos[0]*CELL_SIZE, food_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Отображаем вес еды числом
    weight_text = font.render(str(food_weight), True, YELLOW)
    screen.blit(weight_text, (food_pos[0]*CELL_SIZE + 5, food_pos[1]*CELL_SIZE + 2))

    # Отображаем счёт и уровень
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))

    pygame.display.update()

# Экран окончания игры
def show_game_over_screen():

    screen.fill(BLACK)

    game_over_text = font.render("💥 Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    level_text = font.render(f"Level Reached: {level}", True, WHITE)
    hint_text = font.render("Press ESC to quit...", True, GRAY)

    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    screen.blit(level_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))
    screen.blit(hint_text, (WIDTH // 2 - 100, HEIGHT // 2 + 60))

    pygame.display.update()

    waiting = True
    while waiting:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                waiting = False

# Генерируем первую еду
food = get_food_position()
food_weight = random.randint(1, 3)  # вес еды от 1 до 3
food_timer = FOOD_LIFESPAN  # сбрасываем таймер

running = True
while running:

    clock.tick(speed)

    # Обработка событий выхода
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

    # Управление направлением змейки
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):

        direction = (0, -1)

    elif keys[pygame.K_DOWN] and direction != (0, -1):

        direction = (0, 1)

    elif keys[pygame.K_LEFT] and direction != (1, 0):

        direction = (-1, 0)

    elif keys[pygame.K_RIGHT] and direction != (-1, 0):

        direction = (1, 0)

    # Новая голова змейки
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Проверка столкновений
    if new_head in walls or new_head in snake:

        show_game_over_screen()

        pygame.quit()

        sys.exit()

    snake.insert(0, new_head)

    # Съедание еды
    if new_head == food:

        score += food_weight  # Увеличиваем счёт на значение еды
        food = get_food_position()
        food_weight = random.randint(1, 3)  # новая ценность еды
        food_timer = FOOD_LIFESPAN  # сбрасываем таймер

        # Уровень увеличивается каждые 5 очков
        if score // 5 + 1 > level:

            level += 1
            speed += 2
    else:

        snake.pop()  # если еду не съели — хвост уменьшается

    # Уменьшаем таймер жизни еды
    food_timer -= 1
    if food_timer <= 0:

        food = get_food_position()
        food_weight = random.randint(1, 3)
        food_timer = FOOD_LIFESPAN

    # Отрисовка игры
    draw_game(food)