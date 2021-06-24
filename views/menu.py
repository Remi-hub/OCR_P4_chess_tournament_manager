from models import data_base_manager as dbm


def main_menu() -> str:
    return input(
        f'Hello, welcome to the tournament manager !\nWhat do you want to do? \n'
        f'Press "1" to create a new tournament.\n'
        f'Press "2" to create a new player.\n'
        f'Press "3" to manage the tournament of your choice\n'
        f'Press "4" to show the list of all players.\n'
        # f'Press "5" to assign player to a tournament.\n'
        f'Press "6" to show the list of all tournaments.\n'
        f'Press "0" to quit the program.\n'
    )


def ask_input(question):
    return input(question)


def show_tournaments(all_tournament):
    for tournament in all_tournament:
        print(f"Tournament ID: {tournament.id} - Name: {tournament.name}")


def show_players(all_players):
    for player in all_players:
        print(f"Player ID: {player.id} - Name: {player.first_name} {player.last_name} -  Rating : {player.rating}")


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
    return input(f"Type '1' to add a player to the tournament\n"
                 f"Type '2' to show the list of players by alphabetical order\n"
                 f"Type '3' to show the list of players by rating order\n"
                 f"Type '4' to create the next round\n"
                 f"Type '0' to go back to the main menu\n")


def show_all_players():
    return input(f"Type '1' to show the list of all the players by alphabetical order \n"
                 f"Type '2' to show the list of all the players by rating order\n")


def tournament_menu_response_1():
    player_selection = input('Enter the player ID\n')
    while not player_selection.isdecimal():
        print('Must be integer')
        player_selection = input('Enter the player ID\n')
    return int(player_selection)



def create_player() -> str:
    pass


def error_message(display_error):
    print(display_error)

