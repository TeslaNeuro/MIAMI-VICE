import pygame
import sys
import textwrap

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Vice & Virtue - Scene One")
font = pygame.font.SysFont("Arial", 24)

# --- Load and scale assets ---
background = pygame.image.load("miami_night.jpg")
background = pygame.transform.scale(background, (800, 600))  # Fullscreen fit

portrait = pygame.image.load("detective.png")
portrait = pygame.transform.scale(portrait, (200, 200))  # Resize for layout


# --- Dialogue Data ---
dialogue = [
    "Miami, 1984. Vice cops run the razor's edge between law and temptation.",
    "You're Detective Rico - stylish, sharp, and deep undercover.",
    "The night is heavy with sweat, smoke, and secrets.",
    "A call comes in: body found on the docks. Time to move."
]
dialogue_index = 0

# --- Text wrapping function ---
def draw_wrapped_text(text, font, color, x, y, max_width, surface, line_height=32):
    lines = []
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line, width=50))  # You can adjust width here
    for i, wrapped_line in enumerate(lines):
        text_surface = font.render(wrapped_line, True, color)
        surface.blit(text_surface, (x, y + i * line_height))

# --- Main Loop ---
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(portrait, (20, 350))

    # Draw dialogue box
    pygame.draw.rect(screen, (0, 0, 0), (200, 400, 580, 160))
    pygame.draw.rect(screen, (255, 255, 255), (200, 400, 580, 160), 2)

    # Render wrapped text
    if dialogue_index < len(dialogue):
        draw_wrapped_text(dialogue[dialogue_index], font, (255, 255, 255), 220, 420, 540, screen)

    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if dialogue_index < len(dialogue) - 1:
                dialogue_index += 1
            else:
                print("End of scene")
                running = False

pygame.quit()
sys.exit()
 