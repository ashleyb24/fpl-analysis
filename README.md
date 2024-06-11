# FPL Analysis

## Goals of this project
* Determine if end of season statistics can help predict next season's performance
* Help build squad at start of season
* Recommend transfers based on current form, upcoming opponents etc


## Data required
* List of players for 24/25 season - Not yet available
* Teams for 24/25 season - Not yet available
* Fixtures for 24/25 season - Not yet available
* High level statistics for players over previous seasons - Available but new players for 24/25 will need to be added
* Detailed statistics for players in each game in 23/24 season - Available


## Data structure
* Player
  * Overview of current details: price, team, etc.
  * List of players fetched from ```/bootstrap-static``` API
  * Each entry in ```elements``` is transformed into ```Player``` object
* Season History
  * Overview of each season for each player
  * Player's season history fetched from ```/{player_id}``` API
  * Each entry in ```history_past``` is transformed into ```SeasonHistory``` object
  * ```Player``` has list of ```SeasonHistory``` objects linked
* Game History
  * Detailed game statistics for a player in given season
  * Only available for 23/24 season & future seasons
  * Data for 23/24 season fetched from ```/{player_id}``` API
  * Each entry in ```history``` is transformed into ```GameHistory``` object
  * ```SeasonHistory``` has list of ```GameHistory``` objects linked
* Teams
  * List of teams for each season
  * Only available for 23/24 season & future seasons
  * Data for 23/24 season fetched from ```/bootstrap-static``` API
  * Each entry in ```teams``` is transformed into ```Team``` object