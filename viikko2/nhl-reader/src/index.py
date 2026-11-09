import requests
from player import Player


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    # print("JSON-muotoinen vastaus:")
    # print(response)

    players = []

    for player_dict in response:
        player = Player(player_dict)
        if player.nationality == "FIN":
            players.append(player)

    players.sort(key=lambda player: player.goals + player.assists, reverse=True)
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


main()
