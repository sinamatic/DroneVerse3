import pygame
import sys
from pygame.locals import *
from pygame.math import Vector3

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digitaler Zwilling der Drohne")

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Drohnenklasse
class Drohne:
    def __init__(self):
        self.position = Vector3(WIDTH // 2, HEIGHT // 2, 0)
        self.velocity = Vector3(0, 0, 0)

    def update(self):
        self.position += self.velocity

    def draw(self, screen):
        pygame.draw.circle(
            screen, WHITE, (int(self.position.x), int(self.position.y)), 10
        )


# 3D-Achsen zeichnen
def draw_axes(screen):
    pygame.draw.line(
        screen, WHITE, (WIDTH // 2, HEIGHT // 2), (WIDTH // 2 + 100, HEIGHT // 2), 2
    )  # X-Achse
    pygame.draw.line(
        screen, WHITE, (WIDTH // 2, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2 - 100), 2
    )  # Y-Achse
    pygame.draw.line(
        screen, WHITE, (WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - 70, HEIGHT // 2 + 70), 2
    )  # Z-Achse


# Hauptprogramm
def main():
    clock = pygame.time.Clock()
    drohne = Drohne()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Steuerung der Drohne
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    drohne.velocity.x = -5
                elif event.key == K_RIGHT:
                    drohne.velocity.x = 5
                elif event.key == K_UP:
                    drohne.velocity.y = -5
                elif event.key == K_DOWN:
                    drohne.velocity.y = 5
                elif event.key == K_w:
                    drohne.velocity.z = -5
                elif event.key == K_s:
                    drohne.velocity.z = 5

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT):
                    drohne.velocity.x = 0
                elif event.key in (K_UP, K_DOWN):
                    drohne.velocity.y = 0
                elif event.key in (K_w, K_s):
                    drohne.velocity.z = 0

        drohne.update()

        screen.fill(BLACK)
        draw_axes(screen)
        drohne.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
