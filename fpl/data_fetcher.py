import requests
from models import Player, SeasonHistory, GameHistory, Team
import csv_reader_writer as crw
from typing import List, Tuple
import pandas as pd

_base_url = 'https://fantasy.premierleague.com/api/'


def _get_general_info() -> dict:
    path = 'bootstrap-static/'
    r = requests.get(_base_url + path)
    return r.json()


def _get_player_details(player_id) -> dict:
    path = 'element-summary/' + str(player_id) + '/'
    r = requests.get(_base_url + path)
    return r.json()


def _build_teams(general_info_teams: List[dict], current_season: str) -> List[Team]:
    return [Team(team_data, current_season) for team_data in general_info_teams]


def _build_players(general_info_players: List[dict], team_list: List[Team]) -> List[Player]:
    return [Player(player_data, team_list) for player_data in general_info_players]


def _build_player_history(player: Player, current_season: str) -> None:
    player_details = _get_player_details(player.id)
    season_history_list = []
    for season_history_data in player_details['history_past']:
        season_history = SeasonHistory(player, season_history_data)
        if current_season == season_history.season:
            game_history_list = [GameHistory(season_history, game_data) for game_data in player_details['history']]
            season_history.add_game_history(game_history_list)
        season_history_list.append(season_history)
    player.add_season_history(season_history_list)


def build_data(current_season: str) -> Tuple[List[Team], List[Player]]:
    general_info = _get_general_info()
    team_list = _build_teams(general_info['teams'], current_season)
    player_list = _build_players(general_info['elements'], team_list)
    for player in player_list:
        _build_player_history(player, current_season)
    return team_list, player_list


def build_dataframes(current_season: str, read_from_csv: bool = False, write_to_csv: bool = True) \
        -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    if read_from_csv:
        teams_df = crw.read_from_csv(crw.teams_file_name)
        players_df = crw.read_from_csv(crw.players_file_name)
        season_history_df = crw.read_from_csv(crw.season_history_file_name)
        game_history_df = crw.read_from_csv(crw.game_history_file_name)
    else:
        teams, all_players = build_data(current_season)
        teams_df = pd.DataFrame.from_records([team.to_dict() for team in teams])
        players_df = pd.DataFrame.from_records([player.to_dict() for player in all_players])

        flat_season_history_list = [season.to_dict() for player in all_players for season in player.season_history_list]
        season_history_df = pd.DataFrame.from_records(flat_season_history_list)

        flat_game_history_list = [game.to_dict() for player in all_players
                                  for season in player.season_history_list
                                  for game in season.game_history_list]
        game_history_df = pd.DataFrame.from_records(flat_game_history_list)

    if write_to_csv:
        crw.write_to_csv(teams_df, crw.teams_file_name)
        crw.write_to_csv(players_df, crw.players_file_name)
        crw.write_to_csv(season_history_df, crw.season_history_file_name)
        crw.write_to_csv(game_history_df, crw.game_history_file_name)

    return teams_df, players_df, season_history_df, game_history_df
