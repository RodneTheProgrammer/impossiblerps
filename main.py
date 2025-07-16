
import random

# Full and reduced choices
full_choices = ['fire', 'water', 'grass', 'electric', 'ice', 'dragon']
rage_choices = ['fire', 'water', 'grass']
current_choices = full_choices[:]

# Winning logic
winning_combos = {
    'fire': ['grass', 'ice'],
    'water': ['fire', 'ice'],
    'grass': ['water', 'electric'],
    'electric': ['water', 'ice'],
    'ice': ['grass','dragon'],
    'dragon': ['grass', 'water', 'fire', 'electric']
}

# History and streak tracking
player_history = {}
for choice in full_choices:
    player_history[choice] = 0

player_streak = 0
ai_streak = 0
rage_mode = False
shield_active = False
swap_used = False

def get_winner(player, ai):
    global shield_active
    if player == ai:
        return "Tie"
    elif player in winning_combos[ai]:
        # AI beats player
        if shield_active:
            print("Shield negated the AI's win!")
            return "Player"
        else:
            return "AI"
    else:
        # Player beats AI
        return "Player"

def predict_player_move():
    highest = -1
    predicted = '' # Initialize with an empty string or a default valid choice
    # Ensure current_choices is not empty before iterating
    if not current_choices:
        return random.choice(full_choices) # Fallback if current_choices is empty
        
    # Find the most frequent choice from player history within current_choices
    # Only consider moves that are in current_choices
    valid_moves_in_history = {move: player_history[move] for move in current_choices if move in player_history}

    if not valid_moves_in_history:
        # If no valid moves in history, predict a random choice from current_choices
        return random.choice(current_choices)

    highest_count = -1
    predicted_move = ''

    for move, count in valid_moves_in_history.items():
        if count > highest_count:
            highest_count = count
            predicted_move = move
        elif count == highest_count:
            # If counts are equal, pick randomly between them for less predictability
            predicted_move = random.choice([predicted_move, move])
            
    return predicted_move


def get_ai_move():
    predicted = predict_player_move()
    counters = []
    for move in current_choices:
        # Check if 'move' (AI's potential choice) beats 'predicted' (player's predicted choice)
        if predicted in winning_combos[move]:
            counters.append(move)
            
    if counters:
        ai_choice = random.choice(counters)
    else:
        # Fallback if no direct counter is found, pick randomly
        ai_choice = random.choice(current_choices)
    return ai_choice, predicted


def ai_trash_talk(predicted, actual, ai_move):
    if predicted == actual:
        print("AI: You're too predictable, human. I knew you'd pick " + predicted + ".")
        print("AI: Naturally, I chose " + ai_move + ". Try harder.\n")
    else:
        print("AI: Hmm, unexpected. I thought you'd pick " + predicted + ".")
        print("AI: Lucky move... for now. I went with " + ai_move + ".\n")

def activate_rage_mode():
    global current_choices, rage_mode, shield_active, swap_used
    rage_mode = True
    current_choices = rage_choices[:]
    shield_active = False
    swap_used = False
    print("AI: Enough! I'm done with your fancy 'Ice' and sneaky 'Electric' moves.")
    print("AI: I'm taking away your imagine dragons too. This is rage mode. No freedom.\n I'll imagine draggin deez nuts on your face.")
    print("AI: From now on, it's just Fire. Water. Grass. No mercy.\n")

def check_end_conditions():
    if player_streak >= 5 and ai_streak >= 5:
        print("AI: Seems we're evenly matched. A true stalemate.")
        print("AI: I respect that. Good game, human.")
        return True
    elif player_streak >= 5:
        print("AI: Alright, alright... You're a worthy opponent after all. I concede defeat.")
        print("AI: I'll bow out now. Good game, human!")
        return True
    elif ai_streak >= 5:
        print("AI: This is pointless. You're not even a worthy opponent.")
        print("AI: I'm done wasting my time. Goodbye!")
        return True
    return False

# Intro
print("Welcome to Fire, Water, Grass, Electric, Ice (and Dragon)!")
print("Type 'quit' to exit.\n")

# Main game loop
while True:
    player = raw_input("Choose " + ", ".join(current_choices) + ": ").lower()

    if player == "quit":
        print("AI: Running away? Typical human behavior. Goodbye.")
        break

    if player not in current_choices:
        print("Invalid choice. Try again.\n")
        continue

    player_history[player] += 1
    ai, predicted = get_ai_move()
    ai_trash_talk(predicted, player, ai)

    result = get_winner(player, ai)

    print("You chose:", player)
    print("AI chose:", ai)

    if result == "Tie":
        print("It's a tie!\n")
        player_streak += 1
        ai_streak += 1
    elif result == "Player":
        print("You win this round!\n")
        player_streak += 1
        ai_streak = 0
        if player_streak >= 3 and not rage_mode:
            activate_rage_mode()
    else:
        print("AI wins this round!\n")
        ai_streak += 1
        player_streak = 0

    if check_end_conditions():
        break