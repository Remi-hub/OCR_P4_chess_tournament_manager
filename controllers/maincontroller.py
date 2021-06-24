from models import data_base_manager as dbm
from views import menu
from models.classes.tournament import Tournament
from models.classes.player import Player
from models.classes.round import Round


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
                else:
                    tournament.compute_next_round()
                tournament.list_of_rounds[-1].show_matches_in_round()

            elif response == '5':
                tournament.end_round()
                tournament.list_of_rounds[-1].show_matches_in_round()
            # todo verifier qu'un round a été jouer pour entrer les scores
            # todo ne pas pouvoir rentrer deux fois les scores sur le meme rounds
            # todo créer une commande 5 qui permet de rentrer les scores sur les joueurs du tournois
            # todo call la ligne 30 du main
            # todo avoir laffichage des scores qui s'udaptes, utiliser le score du Tournament ??
            # todo ne pas pouvoir faire plus que 4 rounds ?
            # tournament.list_of_rounds[-1].round_ended()
            elif response == '6':
                menu.show_result(tournament.scores)

                # todo afficher tous les scores
                pass

            elif response == '0':
                exit_menu = True

# def launch_tournament(self):
#     # todo proposer de lancer le tournoi ou de revenir au menu principale
#     launch = get_tournament().compute_next_round()

    def run(self):
        while True:
            response = menu.main_menu()
            if response == "1":
                tournament_name = ""
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
                tournament = Tournament(id, tournament_name, tournament_time_control, tournament_description)
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
                    all_players = sorted(self.player_database, key=lambda player: player.get_name().upper())
                    menu.show_players(all_players)

                if menu_response == '2':
                    all_players = sorted(self.player_database, key=lambda player: player.get_rating(), reverse=True)
                    menu.show_players(all_players)

            # elif response == "5":
            #     tournament_id, player_id = menu.assign_players_to_tournament(self.tournament_database,
            #                                                                  self.player_database)
            #     current_tournament = None
            #     for tournament in self.tournament_database:
            #         if tournament.id == int(tournament_id):
            #             current_tournament = tournament
            #             break
            #     current_player = None
            #     for player in self.player_database:
            #         if player.id == int(player_id):
            #             current_player = player
            #             break

                # current_tournament.add_player(current_player)

            elif response == "6":
                menu.show_tournaments(self.tournament_database)
            elif response == "0":
                return
            else:
                menu.error_message('Invalid choice.')




    ###### quand tu passeras par l'étape d'ajouter des joueurs dans le tournoi
            # tu devras truncate la table tournoi et réinsérer tout les tournois.
