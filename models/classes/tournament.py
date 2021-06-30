from models.classes.player import Player
from models.classes.round import Round
from models.classes.match import Match


def get_matches(players, opponents):
    # check si la longueur de la liste des players est pair, si elle est impair
    # on renvoi une liste vide pour eviter les erreurs (nombre impair de joueur pour faire un match)
    if len(players) % 2 == 1:
        return []
    if len(players) == 0:
        return []
    first_player = players[0]
    # fait une boucle qui commence du deuxieme index de la liste player jusqu'a la fin de la liste player
    for player in players[1:]:
        # si l'id de player n'est pas dans la liste des opponents du premier joueur
        if not player[0] in opponents[first_player[0]]:
            # creation d'une paire qui va contenir notre premier joueur et le joueur ' player ' (de la boucle for, le joueur ' actif ')
            pair = (first_player, player)
            # creation de la liste remaining players sauf le premier player
            remaining_players = players[1:]
            # mise à jour de la liste remaining players en enlevant le player (de la variable pair)
            remaining_players.remove(player)
            # association de la paire avec les paires restantes
            matches = get_matches(remaining_players, opponents)
            # si matches return none c'est qu'il n'y a pas de possiblitées alors on passe joueur suivant
            if matches:
                return [pair] + matches


class Tournament:
    """Model representing a tournament"""
    def __init__(self, id, name, date, time_control, description,
                 total_number_of_rounds=4, ongoing_round=1,
                 players=None, status='initialisation',
                 list_of_rounds=None, scores=None, opponents=None):
        if opponents is None:
            opponents = {}
        if scores is None:
            scores = {}
        if list_of_rounds is None:
            list_of_rounds = []
        if players is None:
            players = []

        self.id = id
        self.name = name
        self.date = date
        self.total_number_of_rounds = total_number_of_rounds
        self.ongoing_round = ongoing_round
        self.players = players
        self.status = status
        self.list_of_rounds = list_of_rounds
        self.scores = scores
        self.opponents = opponents
        self.time_control = time_control
        self.description = description

    def __str__(self):
        return f'{self.name}'

    def serialize(self):

        serialized_tournament = {
            'name': self.name,
            'date': self.date,
            'total_number_of_rounds': self.total_number_of_rounds,
            'ongoing_round': self.ongoing_round,
            'players': [player.id for player in self.players],
            'status': self.status,
            'list_of_rounds': [round.serialize() for
                               round in self.list_of_rounds],
            'scores': self.scores,
            'opponents': self.opponents,
            'time_control': self.time_control,
            'description': self.description

        }
        return serialized_tournament

    def add_player(self, player):
        """adding player in our player list"""
        self.players.append(player)
        self.scores[player.id] = [0, player.rating]
        self.opponents[player.id] = []

    def compute_next_round(self):
        """matching players for the next turn,
         based on ranking for the first round, then by score"""
        if self.ongoing_round == 1:
            self.players = sorted(self.players, key=Player.get_rating,
                                  reverse=True)
            first_half = self.players[:4]
            second_half = self.players[4:]
            list_of_matches = []
            for player_a, player_b in zip(first_half, second_half):
                match = Match('on going', player_a.id, player_b.id)
                list_of_matches.append(match)
            round_one = Round("round 1 | ", 1, list_of_matches)
            self.list_of_rounds.append(round_one)
            self.add_opponent()
            self.ongoing_round += 1

        else:
            sorted_players = sorted(self.scores.items(),
                                    key=lambda item: (item[1][0], item[1][1]),
                                    reverse=True)
            list_of_matches = []
            possibility = get_matches(sorted_players, self.opponents)
            for pair in possibility:
                match = Match('on going', pair[0][0], pair[1][0])
                list_of_matches.append(match)
            next_round = Round(f'round {self.ongoing_round} |',
                               self.ongoing_round, list_of_matches)
            self.list_of_rounds.append(next_round)
            self.add_opponent()
            self.ongoing_round += 1

    def add_opponent(self):
        """fill opponents with last round matches"""
        for match in self.list_of_rounds[-1].list_of_matches:
            if not self.opponents[match.id_player_1].count(match.id_player_2):
                self.opponents[match.id_player_1].append(match.id_player_2)
            if not self.opponents[match.id_player_2].count(match.id_player_1):
                self.opponents[match.id_player_2].append(match.id_player_1)

    def end_round(self):
        self.list_of_rounds[-1].round_ended()
        last_round = self.ongoing_round - 1
        for match in self.list_of_rounds[last_round - 1].list_of_matches:
            self.scores[match.id_player_1][0] += match.score_player_1
            self.scores[match.id_player_2][0] += match.score_player_2
