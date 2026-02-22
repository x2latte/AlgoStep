import pygame
import subprocess
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualization")

# запуск C++ программы и получение состояний массива
proc = subprocess.Popen([".\\bubble_sort.exe"], stdout=subprocess.PIPE, text=True)

steps = []
for line in proc.stdout:
    steps.append(list(map(int, line.strip().split())))

n = len(steps[0])
bar_width = WIDTH // n

running = True
step_idx = 0
clock = pygame.time.Clock()
speed = 5  # кадров в секунду

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if step_idx < len(steps):
        arr = steps[step_idx]
        for i, val in enumerate(arr):
            pygame.draw.rect(screen, (255, 255, 255), 
                             (i*bar_width, HEIGHT-val*50, bar_width-2, val*50))
        step_idx += 1

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
