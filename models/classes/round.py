from datetime import datetime


class Round:
    """Model representing our rounds"""

    def __init__(self, round_name, round_number,
                 list_of_matches, started_at=None, ended_at=None):
        self.round_name = round_name
        self.round_number = int(round_number)
        self.list_of_matches = list_of_matches
        self.started_at = started_at if started_at is not None else\
            datetime.now().strftime("%Y/%m/%d  %H:%M")
        self.ended_at = ended_at

    def __str__(self):
        return f'{self.list_of_matches}'

    def round_ended(self):
        """update ended_at with the actual time"""
        self.ended_at = datetime.now().strftime("%Y/%m/%d  %H:%M")

    def show_matches_in_round(self):
        for match in self.list_of_matches:
            print(f'{self.round_name}', match)

    def serialize(self):
        """serialize a round"""
        serialized_round = {
            'round_name': self.round_name,
            'round_number': self.round_number,
            'list_of_matches': [match.serialize() for
                                match in self.list_of_matches],
            'started_at': self.started_at,
            'ended_at': self.ended_at
        }
        return serialized_round
