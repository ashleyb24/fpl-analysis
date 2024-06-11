import data_fetcher
import pandas as pd
from typing import Dict


def merge_dataframes(left: pd.DataFrame, right: pd.DataFrame, left_on: str, right_on: str) -> pd.DataFrame:
    return pd.merge(left, right, left_on=left_on, right_on=right_on)


def rank_players_per_position(df: pd.DataFrame, season: str, limit: int = 10) -> Dict[str, pd.DataFrame]:
    grouped = df[df['season'] == season].groupby('position')
    players_per_pos = {}
    for pos, group in grouped:
        sorted_group = group.sort_values(by=['total_points'], ascending=False)
        cols = ['name', 'total_points', 'minutes', 'end_cost']
        players_per_pos[pos] = sorted_group[cols][:limit].reset_index(drop=True)
    return players_per_pos


if __name__ == "__main__":
    teams_df, players_df, season_history_df, game_history_df = data_fetcher.build_dataframes('2023/24', True, False)
    detailed_season_history = merge_dataframes(season_history_df, players_df, 'player_id', 'id')
    top_players_per_pos = rank_players_per_position(detailed_season_history, '2023/24')
    for position, top_players in top_players_per_pos.items():
        print('\n Top 10 players in position', position, '\n')
        print(top_players)




