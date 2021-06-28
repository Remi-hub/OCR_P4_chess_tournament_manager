from models import data_base_manager as dbm
from views import menu
from models.classes.tournament import Tournament
from models.classes.player import Player


class MainController:

    def __init__(self):
        self.player_database = dbm.load_player_from_database()
        self.tournament_database = dbm.load_tournament_from_database()

    def get_tournament(self):
        tournament_id = menu.choose_tournament(self.tournament_database)
        for tournament in self.tournament_database:
            if tournament.id == int(tournament_id):
                current_tournament = tournament
                return current_tournament
        return None

    def show_menu_tournament(self, tournament):
        exit_menu = False
        while not exit_menu:
            response = menu.tournament_menu()
            if response == '1':
                if len(tournament.players) == 8:
                    menu.error_message('Tournament is full')
                    return
                menu.show_players(self.player_database)
                player_choice = menu.tournament_menu_response_1()
                for player in self.player_database:
                    if player_choice == player.id:
                        if player in tournament.players:
                            menu.error_message('!!! Player already in the tournament !!! ')
                        else:
                            tournament.add_player(player)
                            dbm.tournaments_table.truncate()
                            dbm.multiple_insert_tournament_in_db(self.tournament_database)
                        break
            elif response == '2':
                sorted_players = sorted(tournament.players, key=lambda item: item.get_name().upper())
                menu.show_players(sorted_players)

            elif response == '3':
                sorted_players = sorted(tournament.players, key=lambda item: item.get_rating(), reverse=True)
                menu.show_players(sorted_players)

            elif response == '4':
                rounds = tournament.list_of_rounds
                if len(rounds) and rounds[-1].ended_at is None:
                    menu.error_message("Previous round not over")
                    tournament.list_of_rounds[-1].show_matches_in_round()
                elif len(rounds) >= tournament.total_number_of_rounds:
                    menu.error_message("Max number of rounds reached")
                else:
                    tournament.compute_next_round()
                    tournament.list_of_rounds[-1].show_matches_in_round()

            elif response == '5':
                if len(tournament.list_of_rounds) == 0:
                    menu.error_message("No round has been played yet\n")
                else:
                    if tournament.list_of_rounds[-1].ended_at is None:
                        tournament.end_round()
                        tournament.list_of_rounds[-1].show_matches_in_round()
                    else:
                        menu.error_message("Scores already entered")

            elif response == '6':
                sorted_result = {key: value for key, value in
                                 sorted(tournament.scores.items(), key=lambda item: item[1], reverse=True)}
                menu.show_result(sorted_result)

            elif response == '7':
                menu.show_matches(tournament.list_of_rounds)

            elif response == '8':
                menu.show_rounds(tournament)

            elif response == '0':
                exit_menu = True

    def run(self):
        global player
        while True:
            response = menu.main_menu()
            if response == "1":
                tournament_name = ""
                tournament_number_of_round = 4
                tournament_time_control = ""
                tournament_description = ""
                valid_input = False
                while not valid_input:
                    tournament_name = menu.ask_input('Enter the tournament name.\n')
                    if tournament_name == "":
                        menu.error_message('Name cannot be empty.\n')
                    else:
                        valid_input = True

                valid_input = False
                while not valid_input:
                    tournament_number_of_round = menu.ask_input(f'Type the number of rounds desired (max 7)\n')
                    if not tournament_number_of_round.isdecimal():
                        menu.error_message("Must be integer")
                    elif not int(tournament_number_of_round) in range(1, 8):
                        menu.error_message("Insert a value between 1 and 7")
                    else:
                        valid_input = True

                valid_input = False
                while not valid_input:
                    tournament_time_control = menu.ask_input(f'select the time control method\n'
                                                             f'"1" for bullet\n'
                                                             f'"2" for blitz\n'
                                                             f'"3" for rapid\n')
                    if tournament_time_control not in ["1", "2", "3"]:
                        menu.error_message('Invalid choice\n')
                    else:
                        valid_input = True

                valid_input = False
                while not valid_input:
                    tournament_description = menu.ask_input(f"Type a description for the tournament\n")
                    if tournament_description == "":
                        menu.error_message('Description cannot be empty.\n')
                    else:
                        valid_input = True

                id = 0 if len(self.tournament_database) == 0 else self.tournament_database[-1].id
                id += 1
                tournament = Tournament(id, tournament_name,
                                        tournament_time_control, tournament_description,
                                        int(tournament_number_of_round))
                dbm.insert_tournament(tournament)
                self.tournament_database.append(tournament)

            elif response == "2":
                player_first_name = ""
                player_last_name = ""
                player_gender = ""
                player_rating = ""

                valid_input = False
                while not valid_input:
                    player_first_name = menu.ask_input("Enter the player first name\n")
                    if player_first_name == "":
                        menu.error_message('Field cannot be empty.\n')
                    else:
                        valid_input = True

                valid_input = False
                while not valid_input:
                    player_last_name = menu.ask_input("Enter the player last name\n")
                    if player_last_name == "":
                        menu.error_message('Field cannot be empty.\n')
                    else:
                        valid_input = True

                valid_input = False
                while not valid_input:
                    player_gender = menu.ask_input("Enter the player gender\n")
                    if player_gender == "":
                        menu.error_message('Field cannot be empty.\n')
                    else:
                        valid_input = True

                valid_input = False
                while not valid_input:
                    player_rating = menu.ask_input("Enter the player rating\n")
                    if player_rating == "":
                        menu.error_message('Field cannot be empty.\n')
                    elif not player_rating.isnumeric():
                        menu.error_message('Answer must be an integer')
                    else:
                        valid_input = True

                id = 0 if len(self.player_database) == 0 else self.player_database[-1].id
                id += 1
                player = Player(id, player_first_name, player_last_name, player_gender, player_rating)
                dbm.insert_player_in_database(player)
                self.player_database.append(player)

            elif response == "3":
                tournament = self.get_tournament()
                print(f'Tournament name : {tournament}')
                if tournament is not None:
                    self.show_menu_tournament(tournament)

            elif response == "4":
                menu_response = menu.show_all_players()

                if menu_response == '1':
                    self.player_database = dbm.load_player_from_database()
                    all_players = sorted(self.player_database, key=lambda player: player.get_name().upper())
                    menu.show_players(all_players)

                if menu_response == '2':
                    self.player_database = dbm.load_player_from_database()
                    all_players = sorted(self.player_database, key=lambda player: player.get_rating(), reverse=True)
                    menu.show_players(all_players)

            elif response == "5":
                all_players = self.player_database
                menu.show_players(all_players)
                id_player = menu.choose_player_by_id()
                found = False
                for player in all_players:
                    if id_player == player.id:
                        found = True
                        new_rating = menu.change_player_rating()
                        dbm.change_player_rating(player.id, new_rating)

                if not found:
                    menu.error_message("Please enter a valid ID\n")



                    # pouvoir choisir un joueur par son ID et modifier son rating
                    # pouvoir selectionner un joueur via son ID
                    # cibler le rating et pouvoir le modifier
                    # sauvegarder le changement?

            elif response == "6":
                menu.show_tournaments(self.tournament_database)

            elif response == "0":
                return
            else:
                menu.error_message('Invalid choice.')


