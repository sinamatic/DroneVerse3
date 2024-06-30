# Sina Steinmüller
# Stand: 2024-06-30
""" 
This program uses Pygame to detect keyboard input and control the drone based on the user's choice.
"""
import pygame
import sys

# Initialisiere Pygame
pygame.init()

# Bildschirmgröße und Farben
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialisiere das Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Keyboard Control")


# Hauptfunktion zur Tastatureingabe und Richtungsaktualisierung
def run_keyboard_control(direction_callback):
    direction = "none"
    direction_changed = False  # Flag, um zu prüfen, ob die Richtung geändert wurde
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not direction_changed:
                    direction = "up"
                    direction_changed = True
                elif event.key == pygame.K_s and not direction_changed:
                    direction = "down"
                    direction_changed = True
                elif event.key == pygame.K_a and not direction_changed:
                    direction = "left"
                    direction_changed = True
                elif event.key == pygame.K_d and not direction_changed:
                    direction = "right"
                    direction_changed = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYUP:
                direction_changed = (
                    False  # Setze das Flag zurück, wenn die Taste losgelassen wird
                )

        direction_callback(direction)

        # Zeichne den Bildschirm (optional)
        screen.fill(WHITE)
        pygame.display.flip()

        clock.tick(60)  # Begrenze die Schleife auf 60 FPS


if __name__ == "__main__":
    # Beispiel für die Verwendung von run_keyboard_control
    def direction_callback(direction):
        print(f"keyboardcontrol.py sagt {direction}")

    run_keyboard_control(direction_callback)
