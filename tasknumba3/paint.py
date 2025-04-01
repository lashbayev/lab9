import pygame
import sys
import math  # Для расчётов при рисовании фигур

pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = WHITE
current_color = BLACK

# Настройки кисти
brush_size = 5
min_brush = 1
max_brush = 50

# Инструменты
TOOL_PENCIL = "pencil"
TOOL_RECTANGLE = "rectangle"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"
TOOL_SQUARE = "square"
TOOL_RIGHT_TRIANGLE = "right_triangle"
TOOL_EQ_TRIANGLE = "equilateral_triangle"
TOOL_RHOMBUS = "rhombus"
tool = TOOL_PENCIL

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint_App")
canvas = pygame.Surface((WIDTH, HEIGHT))  # Создаём холст для сохранения рисунка
canvas.fill(BG_COLOR)
screen.blit(canvas, (0, 0))
clock = pygame.time.Clock()

# Палитра цветов
color_palette = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (255, 255, 255)
]

font = pygame.font.Font(None, 30)

# Отрисовка UI
def draw_ui():
    ui_surface = pygame.Surface((WIDTH, 50))  # Создаём поверхность для UI
    ui_surface.fill(BG_COLOR)  # Заполняем её фоновым цветом
    
    for i, color in enumerate(color_palette):
        pygame.draw.rect(ui_surface, color, (10 + i * 35, 10, 30, 30))

    pygame.draw.rect(ui_surface, (180, 180, 180), (700, 10, 30, 30))
    pygame.draw.rect(ui_surface, (180, 180, 180), (740, 10, 30, 30))

    plus = font.render("+", True, BLACK)
    minus = font.render("-", True, BLACK)
    ui_surface.blit(plus, (707, 10))
    ui_surface.blit(minus, (747, 10))

    label = font.render(f"Brush: {brush_size}", True, BLACK)
    ui_surface.blit(label, (600, 15))
    
    screen.blit(ui_surface, (0, 0))

def get_color_from_palette(pos):
    x, y = pos
    if 10 <= y <= 40:
        for i, color in enumerate(color_palette):
            if 10 + i * 35 <= x <= 10 + i * 35 + 30:
                return color
    return None

drawing = False
start_pos = None

while True:
    clock.tick(FPS)
    screen.blit(canvas, (0, 0))  # Восстанавливаем холст перед отрисовкой UI
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = TOOL_PENCIL
            elif event.key == pygame.K_2:
                tool = TOOL_RECTANGLE
            elif event.key == pygame.K_3:
                tool = TOOL_CIRCLE
            elif event.key == pygame.K_4:
                tool = TOOL_ERASER
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected = get_color_from_palette(event.pos)
                if selected is not None:
                    current_color = selected
                    tool = TOOL_PENCIL if selected != WHITE else TOOL_ERASER
                elif 700 <= event.pos[0] <= 730 and 10 <= event.pos[1] <= 40:
                    brush_size = min(max_brush, brush_size + 1)
                elif 740 <= event.pos[0] <= 770 and 10 <= event.pos[1] <= 40:
                    brush_size = max(min_brush, brush_size - 1)
                else:
                    drawing = True
                    start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                if tool == TOOL_RECTANGLE:
                    pygame.draw.rect(canvas, current_color, pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])), brush_size)
                elif tool == TOOL_CIRCLE:
                    radius = int(math.sqrt((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                drawing = False
    if drawing and tool in [TOOL_PENCIL, TOOL_ERASER]:
        pygame.draw.circle(canvas, current_color, pygame.mouse.get_pos(), brush_size)
    pygame.display.update()
