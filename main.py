import pygame
import sys
from random import randint
import os

from Player import Player
from Game import Game

players = [Player(), Player()]
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

# Game state
state = "start"  # other value: "table"


player1_hand = players[0].get_cards()
player2_hand = players[1].get_cards()
table_cards = [None] * 5



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

def draw_table():
    screen.fill(BLACK)

    # Player 1 (bottom)
    for i, card in enumerate(player1_hand):
        draw_card(500 + i * 100, 550, card.get_str_file())
    label1 = button_font.render("Player 1", True, WHITE)
    screen.blit(label1, (550, 680))

    # Player 2 (top)
    for i, card in enumerate(player2_hand):
        draw_card(500 + i * 100, 50, card.get_str_file())
    label2 = button_font.render("Player 2", True, WHITE)
    screen.blit(label2, (550, 10))

    # Table cards (center)
    for i, card in enumerate(table_cards):
        draw_card(390 + i * 90, 300, card)



def main():
    global state
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "start" and event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    poker_game.start_game()
                    state = "table"

        if state == "start":
            draw_start_screen()
        elif state == "table":
            draw_table()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
