import pygame
import sys

pygame.init()

# Основные параметры экрана и приложения
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = WHITE
current_color = BLACK

# Параметры кисти
brush_size = 5
min_brush = 1
max_brush = 50

# Инструменты рисования
tool = "pencil"
drawing = False
start_pos = None
temp_canvas = None

# Создание окна и холста
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint_App")
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BG_COLOR)

clock = pygame.time.Clock()

# Цветовая палитра
color_palette = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (255, 255, 255)
]

font = pygame.font.Font(None, 30)

def draw_ui():
    """Отрисовка интерфейса пользователя."""
    display_surface.blit(canvas, (0, 0))
    
    # Цветовая палитра
    for i, color in enumerate(color_palette):
        pygame.draw.rect(display_surface, color, (10 + i * 35, 10, 30, 30))
    
    # Кнопки размера кисти
    pygame.draw.rect(display_surface, (180, 180, 180), (700, 10, 30, 30))
    pygame.draw.rect(display_surface, (180, 180, 180), (740, 10, 30, 30))
    
    plus = font.render("+", True, BLACK)
    minus = font.render("-", True, BLACK)
    display_surface.blit(plus, (707, 10))
    display_surface.blit(minus, (747, 10))
    
    label = font.render(f"Brush: {brush_size}", True, BLACK)
    display_surface.blit(label, (600, 15))
    
    # Инструменты
    pygame.draw.rect(display_surface, (200, 200, 200), (10, 50, 100, 30))   # Прямоугольник
    pygame.draw.rect(display_surface, (200, 200, 200), (120, 50, 100, 30))  # Круг
    pygame.draw.rect(display_surface, (200, 200, 200), (230, 50, 100, 30))  # Ластик

    rect_label = font.render("Rect", True, BLACK)
    circle_label = font.render("Circle", True, BLACK)
    eraser_label = font.render("Eraser", True, BLACK)

    display_surface.blit(rect_label, (35, 55))
    display_surface.blit(circle_label, (145, 55))
    display_surface.blit(eraser_label, (250, 55))

    # Новые инструменты
    pygame.draw.rect(display_surface, (200, 200, 200), (340, 50, 100, 30))  # Квадрат
    pygame.draw.rect(display_surface, (200, 200, 200), (450, 50, 100, 30))  # Равносторонний треуг.
    pygame.draw.rect(display_surface, (200, 200, 200), (560, 50, 100, 30))  # Прямоугольный треуг.
    pygame.draw.rect(display_surface, (200, 200, 200), (670, 50, 100, 30))  # Ромб

    square_label = font.render("Square", True, BLACK)
    triangle_label = font.render("Triangle", True, BLACK)
    right_tri_label = font.render("Right T", True, BLACK)
    rhombus_label = font.render("Rhombus", True, BLACK)

    display_surface.blit(square_label, (355, 55))
    display_surface.blit(triangle_label, (465, 55))
    display_surface.blit(right_tri_label, (565, 55))
    display_surface.blit(rhombus_label, (680, 55))

def get_color_from_palette(pos):
    x, y = pos
    if 10 <= y <= 40:
        for i, color in enumerate(color_palette):
            if 10 + i * 35 <= x <= 10 + i * 35 + 30:
                return color
    return None

while True:
    clock.tick(FPS)
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = "pencil"
            elif event.key == pygame.K_2:
                tool = "rectangle"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected = get_color_from_palette(event.pos)
                if selected is not None:
                    current_color = selected
                    tool = "pencil" if selected != WHITE else "eraser"
                elif 700 <= event.pos[0] <= 730 and 10 <= event.pos[1] <= 40:
                    brush_size = min(max_brush, brush_size + 1)
                elif 740 <= event.pos[0] <= 770 and 10 <= event.pos[1] <= 40:
                    brush_size = max(min_brush, brush_size - 1)
                elif 10 <= event.pos[0] <= 110 and 50 <= event.pos[1] <= 80:
                    tool = "rectangle"
                elif 120 <= event.pos[0] <= 220 and 50 <= event.pos[1] <= 80:
                    tool = "circle"
                elif 230 <= event.pos[0] <= 330 and 50 <= event.pos[1] <= 80:
                    tool = "eraser"
                elif 340 <= event.pos[0] <= 440 and 50 <= event.pos[1] <= 80:
                    tool = "square"
                elif 450 <= event.pos[0] <= 550 and 50 <= event.pos[1] <= 80:
                    tool = "triangle"
                elif 560 <= event.pos[0] <= 660 and 50 <= event.pos[1] <= 80:
                    tool = "right_triangle"
                elif 670 <= event.pos[0] <= 770 and 50 <= event.pos[1] <= 80:
                    tool = "rhombus"
                else:
                    drawing = True
                    start_pos = event.pos
                    if tool in ["rectangle", "circle", "square", "triangle", "right_triangle", "rhombus"]:
                        temp_canvas = canvas.copy()

        elif event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil":
                pygame.draw.circle(canvas, current_color, event.pos, brush_size)
            elif tool == "eraser":
                pygame.draw.circle(canvas, BG_COLOR, event.pos, brush_size)
            elif tool in ["rectangle", "circle", "square", "triangle", "right_triangle", "rhombus"] and temp_canvas:
                canvas.blit(temp_canvas, (0, 0))
                x1, y1 = start_pos
                x2, y2 = event.pos

                if tool == "rectangle":
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif tool == "circle":
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                elif tool == "square":
                    side = max(abs(x2 - x1), abs(y2 - y1))
                    rect = pygame.Rect(x1, y1, side, side)
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif tool == "triangle":
                    height = abs(y2 - y1)
                    base = abs(x2 - x1)
                    top = (x1 + base // 2, y1)
                    left = (x1, y1 + height)
                    right = (x1 + base, y1 + height)
                    pygame.draw.polygon(canvas, current_color, [top, left, right], 2)
                elif tool == "right_triangle":
                    pygame.draw.polygon(canvas, current_color, [start_pos, (x2, y1), (x2, y2)], 2)
                elif tool == "rhombus":
                    mid_x = (x1 + x2) // 2
                    mid_y = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    points = [
                        (mid_x, y1),        # Верх
                        (x2, mid_y),        # Право
                        (mid_x, y2),        # Низ
                        (x1, mid_y),        # Лево
                    ]
                    pygame.draw.polygon(canvas, current_color, points, 2)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                temp_canvas = None

    pygame.display.update()
