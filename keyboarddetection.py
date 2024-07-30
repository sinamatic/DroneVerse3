# Maximilian Richter
# Sina Steinmüller
# Stand: 2024-07-26
""" 
This program uses Pygame to detect keyboard input and control the drone based on the user's choice.
"""
import pygame
import sys

keys_pressed = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "takeoff": False,
    "forward": False,
    "backward": False,
}


def run_keyboard_detection(direction_callback):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Keyboard Detection")
    clock = pygame.time.Clock()

    # Hintergrundbild laden und skalieren
    background_image = pygame.image.load("images/DSC01497.jpg")
    background_image = pygame.transform.scale(background_image, (1920, 1080))

    # Schriftarten und -größen definieren
    font_large = pygame.font.SysFont("Arial", 80, bold=True)
    font_small = pygame.font.SysFont("Arial", 48)
    font_textblock = pygame.font.SysFont("Arial", 24)

    running = True
    direction = "none"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    keys_pressed["forward"] = True
                elif event.key == pygame.K_s:
                    keys_pressed["backward"] = True
                elif event.key == pygame.K_a:
                    keys_pressed["left"] = True
                elif event.key == pygame.K_d:
                    keys_pressed["right"] = True
                elif event.key == pygame.K_UP:
                    keys_pressed["up"] = True
                elif event.key == pygame.K_DOWN:
                    keys_pressed["down"] = True
                elif event.key == pygame.K_q:
                    running = False
                    break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys_pressed["forward"] = False
                    direction = "stop"
                elif event.key == pygame.K_s:
                    keys_pressed["backward"] = False
                    direction = "stop"
                elif event.key == pygame.K_a:
                    keys_pressed["left"] = False
                    direction = "stop"
                elif event.key == pygame.K_d:
                    keys_pressed["right"] = False
                    direction = "stop"
                elif event.key == pygame.K_UP:
                    keys_pressed["up"] = False
                    direction = "stop"
                elif event.key == pygame.K_DOWN:
                    keys_pressed["down"] = False
                    direction = "stop"

        try:
            if keys_pressed["up"]:
                direction = "up"
            if keys_pressed["down"]:
                direction = "down"
            if keys_pressed["left"]:
                direction = "left"
            if keys_pressed["right"]:
                direction = "right"
            if keys_pressed["forward"]:
                direction = "forward"
            if keys_pressed["backward"]:
                direction = "backward"

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

        screen.blit(background_image, (0, 0))

        # Überschriften zeichnen
        text_surface = font_large.render("DRONEVERSE", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(960, 65))
        screen.blit(text_surface, text_rect)

        text_surface = font_small.render(
            "You choose keyboard control.", True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=(960, 150))
        screen.blit(text_surface, text_rect)

        # Tastendruck-Ausgabe zeichnen
        text_surface = font_large.render(direction.upper(), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(960, 400))
        screen.blit(text_surface, text_rect)

        # Anweisungs-Textblock zeichnen
        instructions = [
            "Drücke und halte folgende Tasten, damit die Drohne in die gewünschte Richtung fliegt:",
            "w, s = forward, backward",
            "a, d = left, right",
            "Pfeiltasten ↑, ↓  = up, down",
            "no keyinput  = stop",
        ]
        text_y = 780  # Startposition Y für den Textblock
        for line in instructions:
            text_surface = font_textblock.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(960, text_y))
            screen.blit(text_surface, text_rect)
            text_y += 30  # Abstand zwischen den Zeilen

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run_keyboard_detection(
        lambda direction: print(f"keyboarddetection.py sagt {direction}")
    )
