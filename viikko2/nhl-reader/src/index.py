from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import requests
from player import Player


class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()
        return [Player(player_dict) for player_dict in response]


class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scores_by_nationality(self, nationality):
        players = [
            player for player in self.players if player.nationality == nationality
        ]
        players.sort(key=lambda player: player.goals + player.assists, reverse=True)
        return players

    def top_scores_by_team(self, team):
        players = [player for player in self.players if player.team == team]
        players.sort(key=lambda player: player.goals + player.assists, reverse=True)
        return players

    def top_goal_scorers(self, how_many):
        """Palauttaa how_many eniten maaleja tehnyttä pelaajaa maalimäärän mukaan laskevassa järjestyksessä

        Args:
            how_many: Palautettavien pelaajien määrä.
        """
        players = sorted(self.players, key=lambda player: player.goals, reverse=True)
        return players[:how_many]


def main():
    seasons = [
        "2018-19",
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
        "2025-26",
    ]

    nationalities = [
        "USA",
        "FIN",
        "CAN",
        "SWE",
        "CZE",
        "RUS",
        "SLO",
        "FRA",
        "GBR",
        "SVK",
        "DEN",
        "NED",
        "AUT",
        "BLR",
        "GER",
        "SUI",
        "NOR",
        "UZB",
        "LAT",
        "AUS",
    ]

    season = Prompt.ask("Season:", choices=seasons, default="2024-25")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"

    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    filter_by = Prompt.ask(
        "Show players by:", choices=["Team", "Nationality"], default="Team"
    )

    if filter_by == "Team":
        teams = sorted({player.team for player in stats.players})
        selection = Prompt.ask("Team:", choices=teams, default=teams[0])
        players = stats.top_scores_by_team(selection)
    else:
        selection = Prompt.ask("Nationality:", choices=nationalities, default="FIN")
        players = stats.top_scores_by_nationality(selection)

    table = Table(title=f"Season {season} players from {selection}")

    table.add_column("Player", style="magenta")
    table.add_column("Goals", justify="right", style="cyan")
    table.add_column("Assists", justify="right", style="cyan")
    table.add_column("Points", justify="right", style="deep_pink4")

    for player in players:
        score = player.goals + player.assists
        table.add_row(player.name, str(player.goals), str(player.assists), str(score))

    Console().print(table)


if __name__ == "__main__":
    main()
