from typing import List


class Team:
    def __init__(self, team_data: dict, season: str):
        self.id = team_data['id']
        self.season = season
        self.code = team_data['code']
        self.name = team_data['name']
        self.strength = team_data['strength']
        self.strength_attack_away = team_data['strength_attack_away']
        self.strength_attack_home = team_data['strength_attack_home']
        self.strength_defence_away = team_data['strength_defence_away']
        self.strength_defence_home = team_data['strength_defence_home']
        self.strength_overall_away = team_data['strength_overall_away']
        self.strength_overall_home = team_data['strength_overall_home']

    def __repr__(self):
        return f'Team: [id = {self.id}, name = {self.name}, season = {self.season}, code = {self.code}]'

    def __str__(self):
        return f'Team: [id = {self.id}, name = {self.name}]'

    def to_dict(self) -> dict:
        return vars(self)


class Player:
    def __init__(self, element: dict, team_list: List[Team] = None):
        self.id = element['id']
        self.name = element['web_name']
        self.position = element['element_type']
        self.current_price = element['now_cost'] / 10
        self.team_id = element['team']
        self.season_history_list = []
        if team_list is not None:
            self.team = [t for t in team_list if t.id == self.team_id][0]

    def __repr__(self):
        return f'Player: [id = {self.id}, name = {self.name}, team_id = {self.team_id}, position = {self.position}]'

    def __str__(self):
        return f'Player: [id = {self.id}, name = {self.name}]'

    def add_season_history(self, season_history_list: List['SeasonHistory']):
        self.season_history_list.extend(season_history_list)

    def to_dict(self) -> dict:
        all_vars = vars(self)
        exclude = ['season_history_list', 'team']
        return {x: all_vars[x] for x in all_vars if x not in exclude}


class SeasonHistory:
    def __init__(self, player: Player, data: dict):
        self.season = data['season_name']
        self.player = player
        self.player_id = player.id
        self.total_points = data['total_points']
        self.minutes = data['minutes']
        self.clean_sheets = data['clean_sheets']
        self.saves = data['saves']
        self.conceded = data['goals_conceded']
        self.scored = data['goals_scored']
        self.assists = data['assists']
        self.start_cost = data['start_cost'] / 10
        self.end_cost = data['end_cost'] / 10
        self.x_goals = float(data['expected_goals'])
        self.x_assists = float(data['expected_assists'])
        self.x_involvements = float(data['expected_goal_involvements'])
        self.x_conceded = float(data['expected_goals_conceded'])
        self.yellows = data['yellow_cards']
        self.reds = data['red_cards']
        self.influence = float(data['influence'])
        self.creativity = float(data['creativity'])
        self.threat = float(data['threat'])
        self.game_history_list = []

    def __repr__(self):
        return f'SeasonHistory: [season = {self.season}, player_id = {self.player_id}]'

    def __str__(self):
        return f'SeasonHistory: [season = {self.season}, player_id = {self.player_id}]'

    def add_game_history(self, game_history_list: List['GameHistory']):
        self.game_history_list.extend(game_history_list)

    def to_dict(self) -> dict:
        all_vars = vars(self)
        exclude = ['player', 'game_history_list']
        return {x: all_vars[x] for x in all_vars if x not in exclude}


class GameHistory:
    def __init__(self, season: SeasonHistory, data: dict):
        self.season = season
        self.season_name = season.season
        self.player_id = season.player_id
        self.game_id = data['fixture']
        self.opponent = data['opponent_team']
        self.total_points = data['total_points']
        self.minutes = data['minutes']
        self.clean_sheets = data['clean_sheets']
        self.saves = data['saves']
        self.conceded = data['goals_conceded']
        self.scored = data['goals_scored']
        self.assists = data['assists']
        self.cost = data['value'] / 10
        self.x_goals = float(data['expected_goals'])
        self.x_assists = float(data['expected_assists'])
        self.x_involvements = float(data['expected_goal_involvements'])
        self.x_conceded = float(data['expected_goals_conceded'])
        self.yellows = data['yellow_cards']
        self.reds = data['red_cards']
        self.influence = float(data['influence'])
        self.creativity = float(data['creativity'])
        self.threat = float(data['threat'])

    def __repr__(self):
        return f'GameHistory: [season = {self.season_name}, player_id = {self.player_id}, game_id = {self.game_id}]'

    def __str__(self):
        return f'GameHistory: [season = {self.season_name}, player_id = {self.player_id}, game_id = {self.game_id}]'

    def to_dict(self) -> dict:
        all_vars = vars(self)
        exclude = ['season']
        return {x: all_vars[x] for x in all_vars if x not in exclude}
