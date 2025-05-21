import pygame
import sys
import os

from logic.Player import Player
from logic.RandomPlayer import RandomPlayer
from logic.GuiPlayer import GuiPlayer
from logic.Game import Game

players = [GuiPlayer(), RandomPlayer()]
poker_game = Game(small_blind=5, big_blind=10, players=players, start_chips=1000)

# Load card images
card_images = {}
for filename in os.listdir("images"):
    if filename.endswith(".png"):
        key = filename.replace(".png", "")  # e.g., "KH"
        image = pygame.image.load(os.path.join("images", filename))
        image = pygame.transform.scale(image, (80, 120))
        card_images[key] = image

# Init Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poker Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)

# Fonts
title_font = pygame.font.SysFont('Arial', 80)
button_font = pygame.font.SysFont('Arial', 40)
card_font = pygame.font.SysFont('Arial', 32)

# Button
button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 40, 300, 80)

# Action buttons
fold_button = pygame.Rect(WIDTH - 250, HEIGHT - 290, 200, 50)
check_button = pygame.Rect(WIDTH - 250, HEIGHT - 220, 200, 50)
raise_button = pygame.Rect(WIDTH - 250, HEIGHT - 150, 200, 50)
call_button = pygame.Rect(WIDTH - 250, HEIGHT - 80, 200, 50)

# Chip display
player1_chip_display_rect = pygame.Rect(WIDTH - 250, HEIGHT - 360, 200, 50)
player2_chip_display_rect = pygame.Rect(WIDTH - 250, 50, 200, 50)
pot_chip_display_rect = pygame.Rect(50, HEIGHT // 2 - 25, 200, 50)
player1_bet_display_rect = pygame.Rect(50, HEIGHT - 100, 200, 50)
player2_bet_display_rect = pygame.Rect(50, 50, 200, 50)

# Global variables
pot_chips = 0
player1_bet = 0
player2_bet = 0
clicked_decision = None
waiting_for_input = False

# Game state
state = "start"
game_started = False

# Drawing functions
def draw_start_screen():
    screen.fill(BLACK)
    title_text = title_font.render("Poker Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, LIGHT_GRAY if button_rect.collidepoint(mouse_pos) else DARK_GRAY, button_rect)
    button_text = button_font.render("Start Game", True, WHITE)
    screen.blit(button_text, (button_rect.x + 60, button_rect.y + 20))

def draw_card(x, y, code):
    if code and code in card_images:
        screen.blit(card_images[code], (x, y))
    else:
        pygame.draw.rect(screen, WHITE, (x, y, 80, 120), border_radius=8)

def update_table():
    for i, card in enumerate(players[0].get_cards()):
        draw_card(500 + i * 100, 550, card.get_str_file())
    for i, card in enumerate(players[1].get_cards()):
        draw_card(500 + i * 100, 50, card.get_str_file())
    for i, card in enumerate(poker_game.get_table_cards()):
        draw_card(390 + i * 90, 300, card)

def draw_table():
    screen.fill(BLACK)
    draw_action_buttons()
    draw_chip_display(pot_chip_display_rect, f"Pot: {pot_chips}")
    draw_chip_display(player1_bet_display_rect, f"P1 Bet: {player1_bet}")
    draw_chip_display(player2_bet_display_rect, f"P2 Bet: {player2_bet}")

def draw_action_buttons():
    pygame.draw.rect(screen, DARK_GRAY, player1_chip_display_rect, border_radius=10)
    chip_text = button_font.render(f"P1 chips: {players[0].chips}", True, WHITE)
    screen.blit(chip_text, chip_text.get_rect(center=player1_chip_display_rect.center))

    pygame.draw.rect(screen, DARK_GRAY, player2_chip_display_rect, border_radius=10)
    chip_text = button_font.render(f"P2 chips: {players[1].chips}", True, WHITE)
    screen.blit(chip_text, chip_text.get_rect(center=player2_chip_display_rect.center))

    for rect, label in zip([fold_button, check_button, raise_button, call_button], ["Fold", "Check", "Raise", "Call"]):
        pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=10)
        text = button_font.render(label, True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

def draw_chip_display(rect, text):
    pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=10)
    chip_text = button_font.render(text, True, WHITE)
    screen.blit(chip_text, chip_text.get_rect(center=rect.center))

def main():
    global state, game_started, clicked_decision, waiting_for_input, round_state
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "start" and event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    state = "table"
            elif state == "table" and event.type == pygame.MOUSEBUTTONDOWN and waiting_for_input:
                if fold_button.collidepoint(event.pos):
                    clicked_decision = "fold"
                    waiting_for_input = False
                elif check_button.collidepoint(event.pos):
                    clicked_decision = "check"
                    waiting_for_input = False
                elif call_button.collidepoint(event.pos):
                    clicked_decision = "call"
                    waiting_for_input = False
                elif raise_button.collidepoint(event.pos):
                    clicked_decision = "raise 50"  # You can replace with input later
                    waiting_for_input = False

        if state == "start":
            draw_start_screen()
        elif state == "table":
            if not game_started:
                poker_game.start_game()
                game_started = True

            draw_table()
            update_table()


        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
