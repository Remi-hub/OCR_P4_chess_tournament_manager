class Match:

    def __init__(self, status, id_player_1, id_player_2, score_player_1=0, score_player_2=0):
        self.status = status
        self.id_player_1 = id_player_1
        self.id_player_2 = id_player_2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2

    def __str__(self):
        return f'Player {self.id_player_1} ({self.score_player_1} pts) -- VS -- ' \
               f'Player {self.id_player_2} ({self.score_player_2} pts)'

    def scoring(self):
        winner = input(f"Who won the match ? Type "
                       f" '{self.id_player_1}' for player 1,"
                       f" '{self.id_player_2}' for Player 2,"
                       f" Or '0' if there's a draw\n")
                        # todo faire une verif sur les inpouts
                        # todo bouger model mvc; au lieu d'appeler match.scoring acutellement, tu vas appeler match.scoring(winner)

        if str(self.id_player_1) == winner:
            self.score_player_1 = 1

        elif str(self.id_player_2) == winner:
            self.score_player_2 = 1

        else:
            self.score_player_1 = 0.5
            self.score_player_2 = 0.5

        self.status = 'Round ended'

    def serialize(self):

        return [self.status, self.id_player_1, self.id_player_2, self.score_player_1, self.score_player_2]
