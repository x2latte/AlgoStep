import pygame
import random
import time

# Настройки
WIDTH, HEIGHT = 800, 600
ARRAY_SIZE = 30
BAR_WIDTH = WIDTH // ARRAY_SIZE
DELAY = 0.1  # задержка между шагами в секундах

# Инициализация Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Sort Visualization")
clock = pygame.time.Clock()

# Генерация массива
arr = [random.randint(10, HEIGHT-10) for _ in range(ARRAY_SIZE)]

def draw_array(arr, color_positions={}):
    win.fill((0, 0, 0))
    for i, val in enumerate(arr):
        color = (0, 255, 0)  # зелёный
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(win, color, (i * BAR_WIDTH, HEIGHT - val, BAR_WIDTH - 1, val))
    pygame.display.update()

def bubble_sort_visual(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Проверка выхода из окна
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            # Подсветка сравниваемых
            draw_array(arr, {j: (255,0,0), j+1: (255,0,0)})
            time.sleep(DELAY)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw_array(arr, {j: (255,0,0), j+1: (255,0,0)})
                time.sleep(DELAY)
    # Финальный вывод
    draw_array(arr)

# Запуск
running = True
bubble_sort_visual(arr)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
