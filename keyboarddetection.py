# Authors: Sina Steinmüller, Maximilian Richter

""" 
This program uses Pygame to detect keyboard input and control the drone based on the user's choice.
"""
import pygame
import sys


def run_keyboard_detection(direction_callback):
    pygame.init()
    screen = pygame.display.set_mode((1792, 1120))
    pygame.display.set_caption("Keyboard Detection")
    clock = pygame.time.Clock()

    # Hintergrundbild laden und skalieren
    background_image = pygame.image.load("images/DSC01497.jpg")
    background_image = pygame.transform.scale(background_image, (1792, 1120))

    # Schriftarten und -größen definieren
    font_large = pygame.font.SysFont("Arial", 80, bold=True)
    font_small = pygame.font.SysFont("Arial", 48)
    font_textblock = pygame.font.SysFont("Arial", 24)

    running = True
    direction = "none"

    keys_pressed = {
        "up": False,
        "down": False,
        "left": False,
        "right": False,
        "takeoff": False,
        "forward": False,
        "backward": False,
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # KeyDown-Events zur Richtungsbestimmung
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    keys_pressed["forward"] = True
                    direction = "forward"
                elif event.key == pygame.K_s:
                    keys_pressed["backward"] = True
                    direction = "backward"
                elif event.key == pygame.K_a:
                    keys_pressed["left"] = True
                    direction = "left"
                elif event.key == pygame.K_d:
                    keys_pressed["right"] = True
                    direction = "right"
                elif event.key == pygame.K_UP:
                    keys_pressed["up"] = True
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    keys_pressed["down"] = True
                    direction = "down"
                elif event.key == pygame.K_q:
                    running = False

                    break
                direction_callback(direction)

            # KeyUp-Events zum Stoppen der Drohne
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
                direction_callback(direction)

        screen.blit(background_image, (0, 0))

        # Überschriften zeichnen
        text_surface = font_large.render("DRONEVERSE", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(896, 65))
        screen.blit(text_surface, text_rect)

        text_surface = font_small.render(
            "You chose keyboard control.", True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=(896, 150))
        screen.blit(text_surface, text_rect)

        # Tastendruck-Ausgabe zeichnen
        text_surface = font_large.render(direction.upper(), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(896, 400))
        screen.blit(text_surface, text_rect)

        # Anweisungs-Textblock zeichnen
        instructions = [
            "Drücke und halte folgende Tasten, damit die Drohne in die gewünschte Richtung fliegt:",
            "w, s = forward, backward",
            "a, d = left, right",
            "Pfeiltasten ↑, ↓  = up, down",
            "no keyinput  = stop",
        ]
        text_y = 900  # Startposition Y für den Textblock
        for line in instructions:
            text_surface = font_textblock.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(896, text_y))
            screen.blit(text_surface, text_rect)
            text_y += 30  # Abstand zwischen den Zeilen

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run_keyboard_detection(
        lambda direction: print(f"keyboarddetection.py sagt {direction}")
    )
