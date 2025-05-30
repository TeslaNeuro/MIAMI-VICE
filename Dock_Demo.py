import pygame
import sys
import textwrap
import random

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Vice & Virtue")
font = pygame.font.SysFont("Arial", 24)

# --- Load and scale assets ---
backgrounds = {
    "miami_night": pygame.transform.scale(pygame.image.load("miami_night.jpg"), (800, 600)),
    "police_station": pygame.transform.scale(pygame.image.load("police_station.jpg"), (800, 600)),
    "docks": pygame.transform.scale(pygame.image.load("docks_night.jpg"), (800, 600)),
}

portraits = {
    "rico": pygame.transform.scale(pygame.image.load("detective.jpg"), (200, 200)),
    "suspect": pygame.transform.scale(pygame.image.load("suspect.jpg"), (200, 200)),
    "partner": pygame.transform.scale(pygame.image.load("partner.jpg"), (200, 200)),
}

side_events = [
    {
        "id": "corrupt_cop_tip",
        "text": "A stranger brushes past you in the hallway. 'Someone in your squad is dirty,' he whispers.",
        "effect": lambda state: state["clues_found"].append("corrupt cop tip")
    },
    {
        "id": "bloody_photo",
        "text": "A kid hands you a photo soaked in blood. On the back: a name – *Vega*.",
        "effect": lambda state: state["clues_found"].append("bloody photo")
    },
    {
        "id": "police_chief_warning",
        "text": "Chief Martinez pulls you aside. 'Watch Vega. But don’t dig too deep. That’s an order.'",
        "effect": lambda state: state.update({"trust_vega": state["trust_vega"] - 1})
    },
    {
        "id": "flashback",
        "text": "You stare into the neon rain... and remember the last time you saw your brother alive.",
        "effect": lambda state: state.update({"alignment": "vice" if state["alignment"] == "neutral" else state["alignment"]})
    },
    {
        "id": "dead_drop",
        "text": "You find a cassette tape in your locker. Someone wants to talk.",
        "effect": lambda state: state["clues_found"].append("mysterious cassette")
    }
]

# --- Game State ---
game_state = {
    "trust_vega": 0,
    "clues_found": [],
    "alignment": "neutral",
    "side_events_triggered": []
}

# --- Dialogue Data ---
scenes = {
    "scene_1": {
        "background": "miami_night",
        "portrait": "rico",
        "dialogue": [
            "Miami, 1984. Vice cops run the razor's edge between law and temptation.",
            "You're Detective Rico - stylish, sharp, and deep undercover.",
            "The night is heavy with sweat, smoke, and secrets.",
            "A call comes in: body found on the docks. Time to move."
        ],
        "next": "scene_2"
    },
    "scene_2": {
        "background": "police_station",
        "portrait": "partner",
        "dialogue": [
            "At the station, your partner Rockett briefs you on the case.",
            "\"This guy's no small-time dealer,\" he says, pointing to the photo.",
            "\"His name's Carlos Vega. Known for dirty money and worse.\"",
            "You prepare to visit Vega’s last known hangout."
        ],
        "next": "scene_3"
    },
    "scene_3": {
        "background": "docks",
        "portrait": "suspect",
        "dialogue": [
            "The docks are foggy and quiet as you approach Carlos Vega.",
            "He lights a cigarette, eyes cold and calculating.",
            "\"Detective,\" he sneers, \"What brings you to my part of town?\"",
            "\"Cut the games, Vega. Who’s behind the hit?\"",
            "He smirks, \"Maybe it was your own people, detective. You never know who’s playing both sides.\""
        ],
        "choices": [
            "Press Vega harder.",
            "Play it cool and observe."
        ]
    }
}

current_scene = "scene_1"
dialogue_index = 0
choice_made = None

def show_side_event(event_text):
    showing_event = True
    while showing_event:
        screen.fill((0, 0, 0))
        draw_wrapped_text(event_text, font, (255, 255, 255), 100, 250, 600, screen)
        pygame.draw.rect(screen, (255, 255, 255), (80, 230, 640, 140), 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                showing_event = False

# --- Text wrapping function ---
def draw_wrapped_text(text, font, color, x, y, max_width, surface, line_height=32):
    lines = []
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line, width=50))
    for i, wrapped_line in enumerate(lines):
        text_surface = font.render(wrapped_line, True, color)
        surface.blit(text_surface, (x, y + i * line_height))

# --- Draw choices ---
def draw_choices(choices, font, surface):
    base_y = 420
    for i, choice in enumerate(choices):
        choice_text = f"{i + 1}. {choice}"
        text_surface = font.render(choice_text, True, (255, 255, 0))
        surface.blit(text_surface, (220, base_y + i * 40))

# --- Main Loop ---
running = True
while running:
    screen.fill((0, 0, 0))
    scene_data = scenes[current_scene]

    # Draw background and portrait
    bg = backgrounds[scene_data["background"]]
    portrait = portraits[scene_data["portrait"]]
    screen.blit(bg, (0, 0))
    screen.blit(portrait, (20, 350))

    # Draw dialogue box
    pygame.draw.rect(screen, (0, 0, 0), (200, 400, 580, 160))
    pygame.draw.rect(screen, (255, 255, 255), (200, 400, 580, 160), 2)

    # Show dialogue or choices
    if "choices" in scene_data and dialogue_index == len(scene_data["dialogue"]):
        draw_choices(scene_data["choices"], font, screen)
    else:
        if dialogue_index < len(scene_data["dialogue"]):
            draw_wrapped_text(scene_data["dialogue"][dialogue_index], font, (255, 255, 255), 220, 420, 540, screen)

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if "choices" in scene_data and dialogue_index == len(scene_data["dialogue"]):
                # Handle choice input (1 or 2)
                if event.key == pygame.K_1:
                    choice_made = 1
                elif event.key == pygame.K_2:
                    choice_made = 2
                if choice_made:
                    if current_scene == "scene_3":
                        if choice_made == 1:
                            # Press Vega harder
                            scenes["scene_3"]["dialogue"].append(
                                "\"You're lying, Vega. Tell me the truth or I'll make you regret it.\""
                            )
                            scenes["scene_3"]["dialogue"].append(
                                "Vega's smile fades, sweat beads on his forehead."
                            )
                            game_state["trust_vega"] -= 1
                        else:
                            # Play it cool
                            scenes["scene_3"]["dialogue"].append(
                                "You nod slowly, watching him carefully, waiting for a slip."
                            )
                            scenes["scene_3"]["dialogue"].append(
                                "\"Smart move,\" Vega says. \"Maybe we'll talk.\""
                            )
                            game_state["trust_vega"] += 1
                    dialogue_index += 1  # Move dialogue forward after choice
                    choice_made = None

            else:
                # Regular dialogue advance
                dialogue_index += 1
                if dialogue_index >= len(scene_data["dialogue"]):
                    if "choices" in scene_data:
                        # Wait for choice input
                        dialogue_index = len(scene_data["dialogue"])
                    else:
                        # Move to next scene
                        if "next" in scene_data:
                            current_scene = scene_data["next"]
                            # --- Random side event trigger ---
                            if random.random() < 0.5:
                                available_events = [e for e in side_events if e["id"] not in game_state["side_events_triggered"]]
                                if available_events:
                                    event = random.choice(available_events)
                                    game_state["side_events_triggered"].append(event["id"])
                                    event["effect"](game_state)
                                    show_side_event(event["text"])

                            if "next" in scene_data:
                                current_scene = scene_data["next"]
                                dialogue_index = 0
                        else:
                            print("End of story.")
                            running = False

pygame.quit()
sys.exit()
