def main_menu() -> str:
    """Gathering input from the user"""
    return input(
        'Hello, welcome to the tournament manager !\n'
        'What do you want to do? \n'
        'Press "1" to create a new tournament.\n'
        'Press "2" to create a new player.\n'
        'Press "3" to manage the tournament of your choice\n'
        'Press "4" to show the list of all players.\n'
        'Press "5" to change a player rating.\n'
        'Press "6" to show the list of all tournaments.\n'
        'Press "0" to quit the program.\n'
    )


def ask_winner(match):
    """asking the user the winner of a match"""
    while True:
        winner = input(f"Type '{match.id_player_1}' if player 1 won\n"
                       f"Type '{match.id_player_2}' if player 2 won\n"
                       f"Type '0' if there is a draw \n")
        if not winner.isdecimal():
            print("Must be integer")
            continue
        return int(winner)


def ask_input(question):
    return input(question)


def show_tournaments(all_tournament):
    for tournament in all_tournament:
        print(f"Tournament ID: {tournament.id} - Name: {tournament.name}")


def show_players(all_players):
    for player in all_players:
        print(f"Player ID: {player.id} - Name: {player.first_name}"
              f" {player.last_name} -  Rating : {player.rating}")


def assign_players_to_tournament(all_tournament, all_players):
    show_tournaments(all_tournament)
    tournament_id = input("Enter tournament ID\n")
    show_players(all_players)
    player_id = input("Enter player ID\n")
    return tournament_id, player_id


def choose_tournament(tournament):
    show_tournaments(tournament)
    tournament_id = input("Enter tournament ID\n")
    while not tournament_id.isdecimal():
        print('Must be integer')
        tournament_id = input("Enter tournament ID\n")
    return int(tournament_id)


def tournament_menu():
    """Display the menu for a tournament"""
    return input("Type '1' to add a player to the tournament\n"
                 "Type '2' to show the list of players by alphabetical order\n"
                 "Type '3' to show the list of players by rating order\n"
                 "Type '4' to create the next round\n"
                 "Type '5' to enter the scores\n"
                 "Type '6' to show scores\n"
                 "Type '7' to show matches \n"
                 "Type '8' to show rounds\n"
                 "Type '0' to go back to the main menu\n")


def show_all_players():
    return input("Type '1' to show the list of all the players by"
                 " alphabetical order \n"
                 "Type '2' to show the list of all the players by"
                 " rating order\n")


def tournament_menu_response_1():
    """display a submenu for the choice number 1 of tournament_menu"""
    player_selection = input('Enter the player ID\n')
    while not player_selection.isdecimal():
        print('Must be integer')
        player_selection = input('Enter the player ID\n')
    return int(player_selection)


def error_message(display_error):
    print(display_error)


def show_message(message):
    print(message)


def show_result(tournament_scores):
    if len(tournament_scores) >= 1:
        for id, score in tournament_scores.items():
            print(f'Player ID : {id}  --  Score : {score[0]}')
    else:
        print('No data to display\n')


def show_matches(list_of_rounds):
    if len(list_of_rounds) >= 1:
        for round in list_of_rounds:
            print(round.round_name)
            for match in round.list_of_matches:
                print(match)
    else:
        print('No data to display\n')


def show_rounds(tournament):
    if len(tournament.list_of_rounds) >= 1:
        for round in tournament.list_of_rounds:
            print(f'{round.round_name} Round started at :'
                  f' {round.started_at} Round ended at : {round.ended_at}')
    else:
        print('No data to display\n')


def choose_player_by_id():
    player_id = input('Type the ID of the player to modify his rating\n')
    while not player_id.isdecimal():
        print("Must be integer")
        player_id = input('Type the ID of the player to modify his rating\n')
    return int(player_id)


def change_player_rating():
    new_rating = input("What is the new rating for this player ?\n")
    while not new_rating.isdecimal():
        print("Must be integer")
        new_rating = input("What is the new rating for this player ?\n")
    return int(new_rating)
