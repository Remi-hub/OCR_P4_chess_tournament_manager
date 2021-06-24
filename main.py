# from models.classes.player import Player
# from models.classes.tournament import Tournament
# from models import data_base_manager as dbm
from controllers.maincontroller import MainController

#
# def main():
#     # loading the player database
#     player_database = dbm.load_player_from_database()
#     tournament_database = dbm.load_tournament_from_database()
#     new_players = []
#     # give id to players from database
#     id = 0 if len(player_database) == 0 else player_database[-1].id
#     for i in range(0, 8):
#         id += 1
#         player_1 = Player(id, "Henry", "Lecomte", "Homme", 1500)
#         new_players.append(player_1)
#     dbm.multiple_insert_player_in_db(new_players)
#     # adding instance of players in the list of players
#     player_database.extend(new_players)
#     # creating tournament
#     tournament = Tournament("Monaco Grand prix")
#     # adding players to tournament
#     tournament.add_multiple_players(new_players)
#     # print tournament name
#     print("Tournament name : ", tournament)
#     for i in range(0, 4):
#         tournament.compute_next_round()
#         tournament.list_of_rounds[-1].show_matches_in_round()
#         tournament.list_of_rounds[-1].round_ended()
#         print(tournament.opponents)
#     dbm.truncate_tournament()
#     dbm.insert_tournament(tournament)
#
#


def main():
    main_controller = MainController()
    main_controller.run()


if __name__ == '__main__':
    main()

# # todo créer une option pour sorti des menu
# # todo effectuer la serialisation des joueurs / tournois avec tinyDB
# # todo pouvoir modifier le rating des joueurs a n'importe quel moment
# # todo afficher les resulats du tournoi
# # todo pouvoir print la liste de tous les rounds d'un tournoi
# # todo pouvoir print la liste de tous les matchs d'un tournoi
# # todo créer l'interface console du programme
# # todo generer un rapport avec flake8-html a mettre sur le github
# # todo creer un readme avec la maniere de run le programme
