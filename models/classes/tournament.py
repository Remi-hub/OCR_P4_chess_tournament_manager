from models.classes.player import Player
from models.classes.round import Round
from models.classes.match import Match


def get_matches(players, opponents):
    """recursive function to get matches for round 2 and more"""
    if len(players) % 2 == 1:  # checking if players list is pair
        return []
    if len(players) == 0:  # if the list is == 0, we stop creating matches
        return []
    first_player = players[0]
    for player in players[1:]:
        if not player[0] in opponents[first_player[0]]:
            pair = (first_player, player)
            remaining_players = players[1:]
            remaining_players.remove(player)
            pairs = get_matches(remaining_players, opponents)
            if pairs is not None:
                return [pair] + pairs


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
        """serialize the tournament"""
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
                                    #  item[1]==(score, rating)
                                    #  item[1][0] == (score)
                                    #  item[1][1] == (rating)
                                    key=lambda item: (item[1][0], item[1][1]),
                                    reverse=True)
            list_of_matches = []
            matches = get_matches(sorted_players, self.opponents)
            for pair in matches:
                # pair[0][0] == player key == id
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
            # checking if match.id_player_2 is not in opponents of match.id_player_1
            if not self.opponents[match.id_player_1].count(match.id_player_2):
                self.opponents[match.id_player_1].append(match.id_player_2)
            # checking if match.id_player_1 is not in opponents of match.id_player_2
            if not self.opponents[match.id_player_2].count(match.id_player_1):
                self.opponents[match.id_player_2].append(match.id_player_1)

    def end_round(self):
        """finish the round and update the scores """
        self.list_of_rounds[-1].round_ended()
        last_round = self.ongoing_round - 1
        for match in self.list_of_rounds[last_round - 1].list_of_matches:
            self.scores[match.id_player_1][0] += match.score_player_1
            self.scores[match.id_player_2][0] += match.score_player_2
