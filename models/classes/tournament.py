from models.classes.player import Player
from models.classes.round import Round
from models.classes.match import Match


class Tournament:

    """Create a tournament with Name, Number of rounds, players, status, list of rounds and on_going round"""
    def __init__(self, id, name, time_control, description, total_number_of_rounds=4, ongoing_round=1,
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
            'total_number_of_rounds': self.total_number_of_rounds,
            'ongoing_round': self.ongoing_round,
            'players': [player.id for player in self.players],
            'status': self.status,
            'list_of_rounds': [round.serialize() for round in self.list_of_rounds],
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

    def add_multiple_players(self, list_of_players):
        for player in list_of_players:
            self.add_player(player)


    def compute_next_round(self):
        """matching players for the next turn, first round based on ranking, then by score"""
        if self.ongoing_round == 1:
            self.players = sorted(self.players, key=Player.get_rating, reverse=True)
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
            last_round = self.ongoing_round - 1
            for match in self.list_of_rounds[last_round-1].list_of_matches:
                self.scores[match.id_player_1][0] += match.score_player_1
                self.scores[match.id_player_2][0] += match.score_player_2
            # .items() pour créer une liste de tuple contenant la clef et la valeur de mon dict
            # key=lambda sert de clef de tri avec le paramètre item: item[1] (score, rating)
            #  item[1][0] correspond au score et item [1][1] correspond au rating
            sorted_players = sorted(self.scores.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)
            next_round = Round(f'round {self.ongoing_round} |', self.ongoing_round, [])
            self.list_of_rounds.append(next_round)
            self.create_match(sorted_players)
            self.add_opponent()
            self.ongoing_round += 1

    def add_opponent(self):
        """fill opponents with last round matches"""
        for match in self.list_of_rounds[-1].list_of_matches:
            if not self.opponents[match.id_player_1].count(match.id_player_2):
                self.opponents[match.id_player_1].append(match.id_player_2)
            if not self.opponents[match.id_player_2].count(match.id_player_1):
                self.opponents[match.id_player_2].append(match.id_player_1)

    def create_match(self, sorted_players):
        selected_players = []
        for player_1 in sorted_players:
            for player_2 in sorted_players:
                if player_1 != player_2:
                    if player_2[0] not in self.opponents[player_1[0]]:
                        if player_1 not in selected_players and player_2 not in selected_players:
                            selected_players += [player_1, player_2]
                            self.list_of_rounds[self.ongoing_round - 1].list_of_matches.append(
                                Match('on_going', player_1[0], player_2[0])
                            )
    def end_round(self):
        self.list_of_rounds[-1].round_ended()
