import pygame, random, sys

pygame.init()
screen = pygame.display.set_mode((1000, 800)) #Dimensions for game window
pygame.display.set_caption("Lets Go Gambling")
font = pygame.font.SysFont("Georgia", 24)
larger_font = pygame.font.SysFont("Georgia", 48, bold=True)

GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

def get_random_card():
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    random_index = random.randint(0, len(cards) - 1)
    return cards[random_index]

def get_hand_value(hand):
    value = 0
    aces = 0

    for card in hand:
        if card == 'J' or card == 'Q' or card == 'K':
            value += 10
        elif card == 'A':
            aces += 1
            value += 11 #Soft
        else:
            value += int(card)

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1 #Hard

    return value

def draw_text(text, font, color, x, y):
    image = font.render(text, True, color) #Takes string, smooth edges, and color text
    screen.blit(image, (x,y)) #Put image onto screen

def draw_card(card_value, x, y, hidden=False):
    rect = pygame.Rect(x, y, 80, 120) #Create 80x120 card 
    pygame.draw.rect(screen, WHITE, rect, border_radius=5) #Print rect onto screen 
    if hidden:
        #Have blue rect over white rect to hide it
        pygame.draw.rect(screen, BLUE, rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, rect, 3, border_radius=5)
    else:
        #card border for visible cards
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=5)
        if card_value in ['J', 'Q', 'K', 'A']:
            color = RED
        else:
            color = BLACK
        #Print text perfectly in the middle of white rectangle
        text_surface = font.render(card_value, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def main():
    clock = pygame.time.Clock() #Control frame rate

    #Blanks to start off
    player_hand = []
    dealer_hand = []
    state = "playing"
    message = ""

    def starting_game():
        #Restart game board and start new round
        nonlocal player_hand, dealer_hand, state, message
        player_hand = [get_random_card(), get_random_card()]
        dealer_hand = [get_random_card(), get_random_card()]
        state = "playing"
        message = ""

    starting_game()

    run = True
    while run:
        screen.fill(GREEN)

        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)

        for event in pygame.event.get():
            #Click 'X' on the window, quit the game
            if event.type == pygame.QUIT:
                run = False

            #If user presses a key
            if event.type == pygame.KEYDOWN:
                if state == "playing":
                    if event.key == pygame.K_h: #HIT
                        player_hand.append(get_random_card())
                        if get_hand_value(player_hand) > 21:
                            state = "game_over"
                            message = "You Bust! Dealer Wins"

                    elif event.key == pygame.K_s: #STAND
                        #Dealer must draw until they have at least 17
                        while get_hand_value(dealer_hand) < 17:
                            dealer_hand.append(get_random_card())

                        #Recalculates points to see who wins
                        player_value = get_hand_value(player_hand)
                        dealer_value = get_hand_value(dealer_hand)

                        if dealer_value > 21:
                            message = "Dealer Busts! You Win"
                        elif player_value > dealer_value:
                            message = "You Win"
                        elif player_value < dealer_value:
                            message = "Dealer Wins"
                        else:
                            message = "Tie Game"

                        state = "game_over"

                elif state == "game_over":
                    if event.key == pygame.K_y:
                        starting_game()
                    elif event.key == pygame.K_n:
                        run = False

        draw_text("Dealer Hand:", font, WHITE, 50, 50)

        #Loop through dealer's cards and draw them next to each other
        for i, card in enumerate(dealer_hand):
            is_hidden = (i == 1 and state == "playing")
            #moves each pixel so they are next to each other, so no overlap
            draw_card(card, 50 + (i * 90), 100, hidden=is_hidden)

        #Only reveal the dealer's score once game over
        if state != "playing":
            draw_text("Total: " + str(get_hand_value(dealer_hand)), font, WHITE, 50, 230)

        draw_text("Your Hand:", font, WHITE, 50, 320)
        for i, card in enumerate(player_hand):
            draw_card(card, 50 + (i * 90), 370)

        draw_text("Total: " + str(player_value), font, WHITE, 50, 500)

        if state == "playing":
            draw_text("Press 'H' to Hit or 'S' to Stand", font, WHITE, 425, 600)
        elif state == "game_over":
            draw_text(message, larger_font, WHITE, 425, 650)
            draw_text("Play Again? Press 'Y' for Yes or 'N' for No", font, WHITE, 350, 720)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()