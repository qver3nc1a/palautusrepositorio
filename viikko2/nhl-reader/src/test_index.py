import unittest

from index import PlayerStats
from player import Player


class StubPlayerReader:
    def get_players(self):
        return [
            Player(
                {
                    "name": "Nikita Kucherov",
                    "nationality": "RUS",
                    "team": "TBL",
                    "goals": 37,
                    "assists": 84,
                }
            ),
            Player(
                {
                    "name": "Connor McDavid",
                    "nationality": "CAN",
                    "team": "EDM",
                    "goals": 26,
                    "assists": 74,
                }
            ),
            Player(
                {
                    "name": "Leon Draisaitl",
                    "nationality": "GER",
                    "team": "EDM",
                    "goals": 52,
                    "assists": 54,
                }
            ),
        ]


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        self.stats = PlayerStats(StubPlayerReader())

    def test_top_scores_by_nationality_returns_players_in_point_order(self):
        players = self.stats.top_scores_by_nationality("GER")

        self.assertEqual([player.name for player in players], ["Leon Draisaitl"])

    def test_top_scores_by_team_returns_players_in_point_order(self):
        players = self.stats.top_scores_by_team("EDM")

        self.assertEqual(
            [player.name for player in players],
            ["Leon Draisaitl", "Connor McDavid"],
        )

    def test_top_scores_by_team_returns_empty_list_for_unknown_team(self):
        self.assertEqual(self.stats.top_scores_by_team("MIAU"), [])

    def test_top_goal_scorers_returns_requested_number_in_goal_order(self):
        players = self.stats.top_goal_scorers(2)

        self.assertEqual(
            [player.name for player in players],
            ["Leon Draisaitl", "Nikita Kucherov"],
        )


if __name__ == "__main__":
    unittest.main()
