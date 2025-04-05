import pygame, sys, random
from pygame.math import Vector2

# Определение класса змейки
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183,111,122), block_rect)
    
    def move_snake(self):
        if self.new_block:
            self.body.insert(0, self.body[0] + self.direction)
            self.new_block = False
        else:
            self.body = [self.body[0] + self.direction] + self.body[:-1]

    def add_block(self):
        self.new_block = True

# Определение класса еды
class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, self.color, fruit_rect)
    
    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        self.food_type = random.choice(["normal", "gold", "fast"])
        self.timer = pygame.time.get_ticks()
        
        # Установка цвета и очков за разные виды еды
        if self.food_type == "normal":
            self.color = (255, 0, 0)  # Красная еда
            self.value = 1
        elif self.food_type == "gold":
            self.color = (255, 215, 0)  # Золотая еда
            self.value = 3
        elif self.food_type == "fast":
            self.color = (0, 255, 255)  # Голубая еда
            self.value = 2
    
    # Проверка времени исчезновения еды
    def check_timeout(self):
        if pygame.time.get_ticks() - self.timer > 5000:  # 5 секунд
            self.randomize()

# Основной класс игры
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0
        self.level = 1
        self.speed = 150

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.fruit.check_timeout()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.score += self.fruit.value
            self.snake.add_block()
            self.fruit.randomize()
            
            if self.score % 5 == 0:
                self.level += 1
                self.speed = max(50, self.speed - 10)
                pygame.time.set_timer(SCREEN_UPDATE, self.speed)
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()
    
    def draw_grass(self):
        grass_color = (160, 209, 61)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
    
    def draw_score(self):
        score_surface = game_font.render(f'Score: {self.score}  Level: {self.level}', True, (56,74,12))
        screen.blit(score_surface, (10, 10))

# Настройки игры
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 30)

main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, main_game.speed)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 210, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
