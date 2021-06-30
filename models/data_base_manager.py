from tinydb import TinyDB
from tinydb.table import Document
from models.classes.player import Player
from models.classes.match import Match
from models.classes.round import Round
from models.classes.tournament import Tournament

db = TinyDB('db.json')
players_table = db.table('players')
tournaments_table = db.table('tournament')


def load_player_from_database():
    players_document = players_table.all()
    players = []
    for player in players_document:
        player = deserialize_player(player)
        players.append(player)
    return players


def insert_player_in_database(player):

    players_table.insert(Document(player.serialize(), doc_id=player.id))


def insert_tournament(tournament):
    tournaments_table.insert(tournament.serialize())


def multiple_insert_tournament_in_db(tournaments):
    for tournament in tournaments:
        insert_tournament(tournament)


def multiple_insert_player_in_db(players):

    for player in players:
        insert_player_in_database(player)


def get_player(id):
    return players_table.get(doc_id=int(id))


def deserialize_tournament(tournament: Document):
    tournament_id = tournament.doc_id
    name = tournament['name']
    date = tournament['date']
    total_number_of_rounds = tournament['total_number_of_rounds']
    ongoing_round = tournament['ongoing_round']
    players = [deserialize_player(get_player(player_id)) for
               player_id in tournament['players']]
    status = tournament['status']
    list_of_rounds = [deserialize_round(round) for
                      round in tournament['list_of_rounds']]
    scores = {int(key): values for key, values in tournament['scores'].items()}
    opponents = {int(key): values for
                 key, values in tournament['opponents'].items()}
    time_control = tournament['time_control']
    description = tournament['description']
    return Tournament(tournament_id, name, date, time_control, description,
                      total_number_of_rounds, ongoing_round, players,
                      status, list_of_rounds, scores, opponents)


def deserialize_round(round: Document):
    round_name = round['round_name']
    round_number = round['round_number']
    list_of_matches = [deserialize_match(match) for
                       match in round['list_of_matches']]
    started_at = round['started_at']
    ended_at = round['ended_at']
    return Round(round_name, round_number,
                 list_of_matches, started_at, ended_at)


def deserialize_match(match: Document):
    status = match['status']
    id_player_1 = match['id_player_1']
    id_player_2 = match['id_player_2']
    score_player_1 = match['score_player_1']
    score_player_2 = match['score_player_2']
    return Match(status, id_player_1, id_player_2,
                 score_player_1, score_player_2)


def deserialize_player(player: Document):
    first_name = player['first_name']
    last_name = player['last_name']
    gender = player['gender']
    rating = player['rating']
    player_id = player.doc_id
    return Player(player_id, first_name, last_name, gender, rating)


def load_tournament_from_database():
    tournament_document = tournaments_table.all()
    tournaments = []
    for tournament in tournament_document:
        tournament = deserialize_tournament(tournament)
        tournaments.append(tournament)
    return tournaments


def truncate_tournament():
    tournaments_table.truncate()


def truncate_player():
    players_table.truncate()


def change_player_rating(player_id, new_rating):
    players_table.update({'rating': new_rating}, doc_ids=[player_id])
    players_table.all()


def save_tournament(tournament):
    tournaments_table.truncate()
    multiple_insert_tournament_in_db(tournament)
