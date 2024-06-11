import pandas as pd

_folder = '../data/'
teams_file_name = _folder + 'teams.csv'
players_file_name = _folder + 'players.csv'
season_history_file_name = _folder + 'season_history.csv'
game_history_file_name = _folder + 'game_history.csv'
_allowed_file_names = [teams_file_name, players_file_name, season_history_file_name, game_history_file_name]


def write_to_csv(df: pd.DataFrame, file_name: str) -> None:
    if file_name not in _allowed_file_names:
        raise ValueError('Unexpected file name given.')
    df.to_csv(file_name, index=False)


def read_from_csv(file_name: str) -> pd.DataFrame:
    if file_name not in _allowed_file_names:
        raise ValueError('Unexpected file name given.')
    return pd.read_csv(file_name)
