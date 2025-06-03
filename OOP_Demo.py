import pygame
import sys
import random
import time
import json
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
DARK_BLUE = (20, 30, 60)
NEON_PINK = (255, 20, 147)

@dataclass
class GameState:
    trust_vega: int = 0
    corruption_level: int = 0
    reputation: int = 50
    money: int = 1000
    clues_found: List[str] = None
    alignment: str = "neutral"  # neutral, vice, virtue
    side_events_triggered: List[str] = None
    current_scene: str = "intro"
    chapter: int = 1
    endings_unlocked: List[str] = None
    
    def __post_init__(self):
        if self.clues_found is None:
            self.clues_found = []
        if self.side_events_triggered is None:
            self.side_events_triggered = []
        if self.endings_unlocked is None:
            self.endings_unlocked = []

class InteractiveGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Vice & Virtue: Miami Nights")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.fonts = {
            'title': pygame.font.Font(None, 64),
            'subtitle': pygame.font.Font(None, 32),
            'dialogue': pygame.font.Font(None, 24),
            'choice': pygame.font.Font(None, 22),
            'ui': pygame.font.Font(None, 20),
            'stat': pygame.font.Font(None, 18)
        }
        
        # Game state
        self.game_state = GameState()
        self.current_dialogue = []
        self.dialogue_index = 0
        self.choices = []
        self.selected_choice = 0
        self.typing_text = ""
        self.target_text = ""
        self.typing_speed = 3
        self.last_type_time = time.time()
        
        # Visual effects
        self.background_color = DARK_BLUE
        self.rain_drops = self.create_rain()
        self.neon_pulse = 0
        
        # Sound simulation (visual feedback)
        self.screen_shake = 0
        self.flash_effect = 0
        
        # Load game content
        self.load_scenes()
        self.load_side_events()
        
        # Start game
        self.start_scene("intro")
    
    def create_rain(self):
        """Create rain effect for atmosphere"""
        return [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 
                random.randint(1, 3)) for _ in range(50)]
    
    def update_rain(self):
        """Update rain animation"""
        for i, (x, y, speed) in enumerate(self.rain_drops):
            new_y = y + speed * 2
            if new_y > SCREEN_HEIGHT:
                new_y = -10
                x = random.randint(0, SCREEN_WIDTH)
            self.rain_drops[i] = (x, new_y, speed)
    
    def draw_rain(self):
        """Draw rain effect"""
        for x, y, speed in self.rain_drops:
            pygame.draw.line(self.screen, (100, 150, 200), (x, y), (x-2, y+5), 1)
    
    def load_scenes(self):
        """Load all game scenes with rich interactive content"""
        self.scenes = {
            "intro": {
                "background": DARK_BLUE,
                "dialogue": [
                    "MIAMI, 1984",
                    "Neon lights bleed through the perpetual rain...",
                    "You are Detective Rico Martinez - 15 years on the force.",
                    "Tonight, everything changes.",
                    "Your radio crackles: 'Body at the docks. High priority.'"
                ],
                "choices": [
                    ("Rush to the scene immediately", self.choice_rush_docks),
                    ("Stop by the precinct first for backup", self.choice_get_backup),
                    ("Call your partner Tubbs first", self.choice_call_tubbs)
                ]
            },
            
            "docks_alone": {
                "background": (30, 40, 70),
                "dialogue": [
                    "The docks are shrouded in fog and danger.",
                    "You arrive alone - risky, but fast.",
                    "A body lies sprawled near warehouse 47.",
                    "Three bullet holes. Professional job.",
                    "You hear footsteps behind you..."
                ],
                "choices": [
                    ("Draw weapon and turn around", self.choice_draw_weapon),
                    ("Pretend you didn't hear anything", self.choice_ignore_sound),
                    ("Call out 'Police! Show yourself!'", self.choice_announce_police)
                ]
            },
            
            "docks_backup": {
                "background": (30, 40, 70),
                "dialogue": [
                    "You arrive with two patrol officers as backup.",
                    "The extra manpower makes you feel safer.",
                    "The crime scene is pristine - too pristine.",
                    "Officer Johnson finds a briefcase full of cash.",
                    "$50,000 in unmarked bills..."
                ],
                "choices": [
                    ("Report the money immediately", self.choice_report_money),
                    ("Keep quiet and investigate further", self.choice_investigate_money),
                    ("Suggest splitting it with the team", self.choice_corrupt_money)
                ]
            },
            
            "tubbs_meeting": {
                "background": (40, 20, 60),
                "dialogue": [
                    "You meet Tubbs at his usual spot - Carlito's Café.",
                    "'Rico, this case stinks,' he says, lighting a cigarette.",
                    "'Word on the street is Vega's involved.'",
                    "'Carlos Vega - that name should scare you.'",
                    "Tubbs slides you a manila envelope across the table."
                ],
                "choices": [
                    ("Open the envelope immediately", self.choice_open_envelope),
                    ("Ask Tubbs where he got this intel", self.choice_question_tubbs),
                    ("Refuse to look - 'I work clean cases'", self.choice_refuse_envelope)
                ]
            },
            
            "vega_confrontation": {
                "background": (60, 20, 20),
                "dialogue": [
                    "Carlos Vega sits in his penthouse office.",
                    "Expensive suit, cold eyes, danger radiating from every pore.",
                    "'Detective Martinez,' he purrs, 'I've been expecting you.'",
                    "'That body at the docks... unfortunate business.'",
                    "He opens a briefcase. It's full of money."
                ],
                "choices": [
                    ("'You're under arrest for murder!'", self.choice_arrest_vega),
                    ("'I'm listening...' (hear his offer)", self.choice_listen_vega),
                    ("'I know what you did' (bluff)", self.choice_bluff_vega)
                ]
            },
            
            "final_choice": {
                "background": (80, 10, 10),
                "dialogue": [
                    "FINAL DECISION",
                    "Everything has led to this moment.",
                    f"Your corruption level: {self.game_state.corruption_level}",
                    f"Your reputation: {self.game_state.reputation}",
                    "Vega's operation is exposed. What do you do?"
                ],
                "choices": [
                    ("Arrest everyone - be the hero cop", self.ending_hero),
                    ("Take the money and disappear", self.ending_corrupt),
                    ("Try to find a middle ground", self.ending_compromise)
                ]
            }
        }
    
    def load_side_events(self):
        """Load random side events that add depth"""
        self.side_events = [
            {
                "id": "informant_tip",
                "text": "A nervous informant approaches: 'Detective, someone in your precinct is feeding info to Vega.'",
                "effect": lambda: self.add_clue("corrupt_cop_tip"),
                "trigger_chance": 0.3
            },
            {
                "id": "family_call", 
                "text": "Your ex-wife calls: 'Rico, our daughter needs you to be the good guy this time.'",
                "effect": lambda: self.modify_stats(reputation=10),
                "trigger_chance": 0.2
            },
            {
                "id": "bribe_attempt",
                "text": "A well-dressed man slips you an envelope: 'For your discretion, detective.'",
                "choices": [
                    ("Take the money (+$5000, +corruption)", lambda: self.modify_stats(money=5000, corruption_level=15)),
                    ("Refuse and report it (+reputation)", lambda: self.modify_stats(reputation=15))
                ],
                "trigger_chance": 0.4
            },
            {
                "id": "witness_intimidation",
                "text": "You find a potential witness. They're terrified: 'Please don't make me testify!'",
                "choices": [
                    ("Promise protection (+reputation)", lambda: self.modify_stats(reputation=10)),
                    ("Threaten them for info (+clue, +corruption)", lambda: (self.add_clue("witness_statement"), self.modify_stats(corruption_level=10))),
                    ("Let them go (-reputation)", lambda: self.modify_stats(reputation=-5))
                ],
                "trigger_chance": 0.3
            }
        ]
    
    def start_scene(self, scene_name: str):
        """Start a new scene"""
        self.game_state.current_scene = scene_name
        scene = self.scenes.get(scene_name)
        if scene:
            self.current_dialogue = scene["dialogue"][:]
            self.choices = scene.get("choices", [])
            self.dialogue_index = 0
            self.selected_choice = 0
            self.background_color = scene.get("background", DARK_BLUE)
            self.start_typing_next_dialogue()
            
            # Trigger random side events
            self.maybe_trigger_side_event()
    
    def maybe_trigger_side_event(self):
        """Randomly trigger side events for more dynamic gameplay"""
        available_events = [e for e in self.side_events 
                          if e["id"] not in self.game_state.side_events_triggered]
        
        for event in available_events:
            if random.random() < event["trigger_chance"]:
                self.game_state.side_events_triggered.append(event["id"])
                self.trigger_side_event(event)
                break
    
    def trigger_side_event(self, event):
        """Handle side event"""
        if "choices" in event:
            # Side event with choices
            self.show_side_event_with_choices(event)
        else:
            # Simple side event
            self.show_side_event_message(event["text"])
            if "effect" in event:
                event["effect"]()
    
    def show_side_event_message(self, message):
        """Show a side event message"""
        self.flash_effect = 30  # Visual flash
        # In a full implementation, this would be a modal dialog
        print(f"SIDE EVENT: {message}")  # Temporary console output
    
    def show_side_event_with_choices(self, event):
        """Show side event with choices"""
        # This would be implemented as a modal dialog in the full version
        print(f"SIDE EVENT: {event['text']}")
        for i, (choice_text, effect) in enumerate(event["choices"]):
            print(f"{i+1}. {choice_text}")
    
    def start_typing_next_dialogue(self):
        """Start typing animation for next dialogue line"""
        if self.dialogue_index < len(self.current_dialogue):
            self.target_text = self.current_dialogue[self.dialogue_index]
            self.typing_text = ""
            self.last_type_time = time.time()
    
    def update_typing(self):
        """Update typing animation"""
        current_time = time.time()
        if (current_time - self.last_type_time > 1.0 / self.typing_speed and 
            len(self.typing_text) < len(self.target_text)):
            self.typing_text += self.target_text[len(self.typing_text)]
            self.last_type_time = current_time
    
    def modify_stats(self, **kwargs):
        """Modify game state stats"""
        for stat, value in kwargs.items():
            if hasattr(self.game_state, stat):
                current_value = getattr(self.game_state, stat)
                setattr(self.game_state, stat, current_value + value)
                
        # Clamp reputation and corruption
        self.game_state.reputation = max(0, min(100, self.game_state.reputation))
        self.game_state.corruption_level = max(0, min(100, self.game_state.corruption_level))
        
        # Update alignment based on corruption
        if self.game_state.corruption_level > 60:
            self.game_state.alignment = "vice"
        elif self.game_state.corruption_level < 20 and self.game_state.reputation > 70:
            self.game_state.alignment = "virtue"
        else:
            self.game_state.alignment = "neutral"
    
    def add_clue(self, clue: str):
        """Add a clue to the investigation"""
        if clue not in self.game_state.clues_found:
            self.game_state.clues_found.append(clue)
            self.flash_effect = 15  # Visual feedback
    
    # Choice handlers - these make the game truly interactive
    def choice_rush_docks(self):
        self.modify_stats(corruption_level=5)  # Reckless behavior
        self.start_scene("docks_alone")
    
    def choice_get_backup(self):
        self.modify_stats(reputation=10)  # Professional approach
        self.start_scene("docks_backup")
    
    def choice_call_tubbs(self):
        self.modify_stats(reputation=5)
        self.start_scene("tubbs_meeting")
    
    def choice_draw_weapon(self):
        self.modify_stats(corruption_level=10)
        self.add_clue("aggressive_approach")
        self.current_dialogue = ["You spin around, gun drawn!", 
                               "It's just a stray cat. Your nerves are shot.",
                               "But you notice fresh tire tracks in the mud..."]
        self.dialogue_index = 0
        self.start_typing_next_dialogue()
    
    def choice_ignore_sound(self):
        self.modify_stats(corruption_level=-5, reputation=5)
        self.add_clue("observed_quietly")
        self.current_dialogue = ["You continue examining the body.",
                               "Patience pays off - you spot a crucial detail.",
                               "A business card tucked in the victim's shoe."]
        self.dialogue_index = 0
        self.start_typing_next_dialogue()
    
    def choice_announce_police(self):
        self.modify_stats(reputation=10)
        self.current_dialogue = ["'POLICE! SHOW YOURSELF!'",
                               "A figure emerges from the shadows...",
                               "It's your informant, Pedro. He's terrified."]
        self.dialogue_index = 0
        self.start_typing_next_dialogue()
    
    def choice_report_money(self):
        self.modify_stats(reputation=20, corruption_level=-10)
        self.add_clue("clean_money_trail")
        self.start_scene("vega_confrontation")
    
    def choice_investigate_money(self):
        self.modify_stats(reputation=5)
        self.add_clue("suspicious_money")
        self.start_scene("vega_confrontation")
    
    def choice_corrupt_money(self):
        self.modify_stats(money=16666, corruption_level=25, reputation=-15)
        self.start_scene("vega_confrontation")
    
    def choice_open_envelope(self):
        self.add_clue("vega_photos")
        self.modify_stats(reputation=5)
        self.start_scene("vega_confrontation")
    
    def choice_question_tubbs(self):
        self.modify_stats(reputation=10)
        self.add_clue("tubbs_source")
        self.start_scene("vega_confrontation")
    
    def choice_refuse_envelope(self):
        self.modify_stats(reputation=15, corruption_level=-10)
        self.start_scene("vega_confrontation")
    
    def choice_arrest_vega(self):
        self.modify_stats(reputation=25)
        self.start_scene("final_choice")
    
    def choice_listen_vega(self):
        self.modify_stats(corruption_level=15)
        self.start_scene("final_choice")
    
    def choice_bluff_vega(self):
        self.modify_stats(reputation=10)
        self.start_scene("final_choice")
    
    def ending_hero(self):
        self.game_state.endings_unlocked.append("hero")
        self.show_ending("HERO ENDING", "You cleaned up Miami, one arrest at a time.")
    
    def ending_corrupt(self):
        self.game_state.endings_unlocked.append("corrupt")
        self.show_ending("CORRUPTION ENDING", "Money talks. You listened.")
    
    def ending_compromise(self):
        self.game_state.endings_unlocked.append("compromise")
        self.show_ending("GRAY ENDING", "Sometimes the line between right and wrong is blurred.")
    
    def show_ending(self, title, description):
        """Show game ending"""
        self.current_dialogue = [title, description, 
                               f"Final Stats - Reputation: {self.game_state.reputation}",
                               f"Corruption: {self.game_state.corruption_level}",
                               f"Money: ${self.game_state.money}",
                               f"Clues Found: {len(self.game_state.clues_found)}",
                               "Press R to restart or Q to quit"]
        self.choices = []
        self.dialogue_index = 0
        self.start_typing_next_dialogue()
    
    def draw_background(self):
        """Draw atmospheric background"""
        self.screen.fill(self.background_color)
        
        # Add screen shake effect
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # Draw rain
        self.draw_rain()
        
        # Add neon glow effects
        self.neon_pulse += 0.1
        glow_intensity = int(50 + 30 * abs(pygame.math.Vector2(1, 0).rotate(self.neon_pulse * 180 / 3.14159).x))
        
        # Draw neon city silhouette
        for i in range(5):
            height = random.randint(100, 300)
            color = (glow_intensity // 3, glow_intensity // 2, glow_intensity)
            pygame.draw.rect(self.screen, color, 
                           (i * 240 + shake_x, SCREEN_HEIGHT - height + shake_y, 200, height))
    
    def draw_dialogue_box(self):
        """Draw the main dialogue interface"""
        # Main dialogue box
        dialogue_rect = pygame.Rect(50, SCREEN_HEIGHT - 250, SCREEN_WIDTH - 100, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), dialogue_rect)
        pygame.draw.rect(self.screen, WHITE, dialogue_rect, 3)
        
        # Draw current dialogue
        if self.typing_text:
            lines = self.wrap_text(self.typing_text, self.fonts['dialogue'], SCREEN_WIDTH - 120)
            y_offset = SCREEN_HEIGHT - 230
            for line in lines:
                text_surface = self.fonts['dialogue'].render(line, True, WHITE)
                self.screen.blit(text_surface, (70, y_offset))
                y_offset += 30
        
        # Draw choices
        if self.choices and self.dialogue_index >= len(self.current_dialogue):
            choice_y = SCREEN_HEIGHT - 180
            for i, (choice_text, _) in enumerate(self.choices):
                color = YELLOW if i == self.selected_choice else WHITE
                if i == self.selected_choice:
                    # Highlight selected choice
                    highlight_rect = pygame.Rect(65, choice_y - 2, 600, 25)
                    pygame.draw.rect(self.screen, (50, 50, 100), highlight_rect)
                
                choice_surface = self.fonts['choice'].render(f"{i+1}. {choice_text}", True, color)
                self.screen.blit(choice_surface, (70, choice_y))
                choice_y += 30
    
    def draw_stats_panel(self):
        """Draw player stats"""
        panel_rect = pygame.Rect(SCREEN_WIDTH - 300, 20, 270, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        stats = [
            f"Chapter: {self.game_state.chapter}",
            f"Reputation: {self.game_state.reputation}/100",
            f"Corruption: {self.game_state.corruption_level}/100", 
            f"Money: ${self.game_state.money}",
            f"Alignment: {self.game_state.alignment.upper()}",
            f"Clues: {len(self.game_state.clues_found)}",
            f"Trust Vega: {self.game_state.trust_vega}"
        ]
        
        y_offset = 40
        for stat in stats:
            # Color code some stats
            color = WHITE
            if "Reputation" in stat:
                color = GREEN if self.game_state.reputation > 50 else RED
            elif "Corruption" in stat:
                color = RED if self.game_state.corruption_level > 50 else GREEN
            elif "Alignment" in stat:
                if "VIRTUE" in stat:
                    color = GREEN
                elif "VICE" in stat:
                    color = RED
                else:
                    color = YELLOW
                    
            text_surface = self.fonts['stat'].render(stat, True, color)
            self.screen.blit(text_surface, (SCREEN_WIDTH - 290, y_offset))
            y_offset += 22
    
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Wrap text to fit within specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def handle_input(self, event):
        """Handle player input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Advance dialogue
                if len(self.typing_text) < len(self.target_text):
                    # Skip typing animation
                    self.typing_text = self.target_text
                else:
                    self.dialogue_index += 1
                    if self.dialogue_index < len(self.current_dialogue):
                        self.start_typing_next_dialogue()
                    elif self.choices:
                        # Show choices
                        pass
                    
            elif event.key == pygame.K_UP:
                if self.choices:
                    self.selected_choice = (self.selected_choice - 1) % len(self.choices)
                    
            elif event.key == pygame.K_DOWN:
                if self.choices:
                    self.selected_choice = (self.selected_choice + 1) % len(self.choices)
                    
            elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                # Number key choice selection
                choice_num = event.key - pygame.K_1
                if self.choices and choice_num < len(self.choices):
                    choice_text, choice_func = self.choices[choice_num]
                    choice_func()
                    
            elif event.key == pygame.K_RETURN and self.choices:
                # Execute selected choice
                if self.selected_choice < len(self.choices):
                    choice_text, choice_func = self.choices[self.selected_choice]
                    choice_func()
                    
            elif event.key == pygame.K_r:
                # Restart game
                self.game_state = GameState()
                self.start_scene("intro")
                
            elif event.key == pygame.K_q:
                # Quit
                self.running = False
                
            elif event.key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LCTRL]:
                # Save game
                self.save_game()
                
            elif event.key == pygame.K_l and pygame.key.get_pressed()[pygame.K_LCTRL]:
                # Load game
                self.load_game()
    
    def save_game(self):
        """Save current game state"""
        try:
            save_data = {
                'trust_vega': self.game_state.trust_vega,
                'corruption_level': self.game_state.corruption_level,
                'reputation': self.game_state.reputation,
                'money': self.game_state.money,
                'clues_found': self.game_state.clues_found,
                'alignment': self.game_state.alignment,
                'side_events_triggered': self.game_state.side_events_triggered,
                'current_scene': self.game_state.current_scene,
                'chapter': self.game_state.chapter,
                'endings_unlocked': self.game_state.endings_unlocked
            }
            with open('vice_virtue_save.json', 'w') as f:
                json.dump(save_data, f, indent=2)
            print("Game saved!")
        except Exception as e:
            print(f"Save failed: {e}")
    
    def load_game(self):
        """Load saved game state"""
        try:
            with open('vice_virtue_save.json', 'r') as f:
                save_data = json.load(f)
            
            # Restore game state
            for key, value in save_data.items():
                setattr(self.game_state, key, value)
            
            # Restart the current scene
            self.start_scene(self.game_state.current_scene)
            print("Game loaded!")
        except Exception as e:
            print(f"Load failed: {e}")
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_input(event)
            
            # Update animations
            self.update_typing()
            self.update_rain()
            
            # Decrease effects
            if self.screen_shake > 0:
                self.screen_shake -= 1
            if self.flash_effect > 0:
                self.flash_effect -= 1
            
            # Draw everything
            self.draw_background()
            
            # Flash effect
            if self.flash_effect > 0:
                flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                flash_surface.set_alpha(self.flash_effect * 5)
                flash_surface.fill(WHITE)
                self.screen.blit(flash_surface, (0, 0))
            
            self.draw_dialogue_box()
            self.draw_stats_panel()
            
            # Draw controls hint
            controls_text = "SPACE/ENTER: Continue | ↑↓: Select | 1-9: Quick Choice | Ctrl+S: Save | R: Restart"
            control_surface = self.fonts['ui'].render(controls_text, True, (150, 150, 150))
            self.screen.blit(control_surface, (20, SCREEN_HEIGHT - 25))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = InteractiveGame()
    game.run()
