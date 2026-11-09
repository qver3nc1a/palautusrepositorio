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


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scores_by_nationality("FIN")
    for player in players:
        print(
            "Name:",
            player.name,
            "| Nationality:",
            player.nationality,
            "| Score:",
            player.goals,
            "+",
            player.assists,
            "=",
            player.goals + player.assists,
        )


if __name__ == "__main__":
    main()
