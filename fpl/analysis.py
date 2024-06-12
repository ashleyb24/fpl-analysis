import data_fetcher
import pandas as pd
from typing import Dict, List, Callable


def merge_dataframes(left: pd.DataFrame, right: pd.DataFrame, left_on: str, right_on: str) -> pd.DataFrame:
    return pd.merge(left, right, left_on=left_on, right_on=right_on)


def filter_group_and_sort_df(df: pd.DataFrame, filter_cond: Callable,
                             group_by: str, limit: int = 10, log: bool = True) -> Dict[str, pd.DataFrame]:
    grouped = df.loc[filter_cond].groupby(group_by)
    ranked_players_by_group = {}
    for x, group in grouped:
        sorted_group = group.sort_values(by=['total_points'], ascending=False)
        cols = ['name', 'total_points', 'minutes', 'end_cost']
        ranked_players_by_group[x] = sorted_group[cols][:limit].reset_index(drop=True)
        if log:
            print('\n Top 10 players in', group_by, x, '\n')
            print(ranked_players_by_group[x])
    return ranked_players_by_group


def rank_players_per_position(df: pd.DataFrame, season: str, limit: int, log: bool) -> Dict[str, pd.DataFrame]:
    return filter_group_and_sort_df(df, lambda x: x['season'] == season, 'position', limit, log)


def rank_players_in_pos_per_year(df: pd.DataFrame, season_lst: List[str],
                                 pos: int, limit: int, log: bool) -> Dict[str, pd.DataFrame]:
    return filter_group_and_sort_df(df, lambda x: (x['position'] == pos) & (x['season'].isin(season_lst)),
                                    'season', limit, log)


if __name__ == "__main__":
    teams_df, players_df, season_history_df, game_history_df = data_fetcher.build_dataframes('2023/24', True, False)
    detailed_season_history = merge_dataframes(season_history_df, players_df, 'player_id', 'id')
    top_players_per_pos = rank_players_per_position(detailed_season_history, '2023/24', 10, True)
    seasons = ['2021/22', '2022/23', '2023/24']
    top_gks_per_year = rank_players_in_pos_per_year(detailed_season_history, seasons, 1, 10, True)




