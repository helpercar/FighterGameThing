# Example file showing a basic pygame "game loop"
# Example Code expanded from https://www.pygame.org/docs/
import pygame
import fight
import classes
import random
import sys

scroll_index = 0
lines = 4

def refresh(max_hp1, max_hp2, selected_attack, fight1):
    # Refresh the screen using the updated health values and selected attacks
    screen.fill("teal")
    pygame.draw.circle(screen, "red", (200, 360), 40)
    pygame.draw.circle(screen, "blue", (1080, 360), 40)
    pygame.draw.rect(screen, "green", (150, 275, fight1.fighter1.health, 20))
    pygame.draw.rect(screen, "green", (1030, 275, fight1.fighter2.health, 20))
    pygame.draw.rect(screen, "white", (150, 275, max_hp1, 20), 2)
    pygame.draw.rect(screen, "white", (1030, 275, max_hp2, 20), 2)

    attacks = fight1.fighter1.get_attacks()
    
    font = pygame.font.Font(None, 36)
    
    if selected_attack > 3:
        scroll_index = selected_attack - 3
    else:
        scroll_index = 0

    pygame.draw.rect(screen, "gray", (35, 30, 180, 204))
    pygame.draw.rect(screen, "white", (40, 35, 170, 194))

    for i, attack in enumerate(attacks):
        if i < scroll_index or i > scroll_index + 3: # Range of [scroll_index, scroll_index + 3] for 4 items
            continue
        text = font.render(attack, True, "cyan" if i == selected_attack else "black")
        screen.blit(text, (50, 50 + (i - scroll_index) * 40))

    pygame.display.flip()

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Start at Center
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


while running:
    # Create a fight once and run it inside the main loop
    print("Fight")
    slime1 = classes.Slime(health=125, attack=12, defense=5, speed=10, name="Slime1", level=1)
    slime2 = classes.Slime(health=100, attack=10, defense=5, speed=10, name="Slime2", level=1)
    fight1 = fight.fight(slime1, slime2)
    attacks = fight1.fighter1.get_attacks()
    print(attacks)
    font = pygame.font.Font(None, 36)
    max_hp1 = fight1.fighter1.health
    max_hp2 = fight1.fighter2.health
    selected_attack = 0
    chosen = False
    
    refresh(max_hp1, max_hp2, selected_attack, fight1)
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop.

    while fight1.fighter1.health > 0 and fight1.fighter2.health > 0:
        current_fighter = fight1.turn_order()
        chosen = False
        
        if (current_fighter == 1):
            print("Player's Turn")
            while not chosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif current_fighter == 1:
                            if event.key in (pygame.K_s, pygame.K_DOWN):
                                selected_attack = (selected_attack + 1) % len(attacks)
                                refresh(max_hp1, max_hp2, selected_attack, fight1)
                                dt = clock.tick(60) / 1000  # Amount of seconds between each loop.
                            elif event.key in (pygame.K_w, pygame.K_UP):
                                selected_attack = (selected_attack - 1) % len(attacks)
                                refresh(max_hp1, max_hp2, selected_attack, fight1)
                                dt = clock.tick(60) / 1000  # Amount of seconds between each loop.
                            elif event.key == pygame.K_SPACE:
                                print("Selected Attack: " + attacks[selected_attack])
                                damage = fight1.fighter1.choice_attack(selected_attack)
                                fight1.attack(fight1.fighter2, damage)
                                current_fighter = fight1.turn_order()
                                chosen = True
        else:
            print("Enemy's Turn")
            enemy_index = random.randrange(len(fight1.fighter2.get_attacks()))
            damage = fight1.fighter2.choice_attack(enemy_index)
            fight1.attack(fight1.fighter1, damage)
            current_fighter = fight1.turn_order()

        refresh(max_hp1, max_hp2, selected_attack, fight1)
        dt = clock.tick(60) / 1000  # Amount of seconds between each loop.

    refresh(max_hp1, max_hp2, selected_attack, fight1)
    pygame.time.delay(1000)


pygame.quit()

