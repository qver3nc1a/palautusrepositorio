import unittest
from player import Player
from statistics_service import StatisticsService


class StubPlayerReader:
    def get_players(self):
        return [
            Player("Nikita Kucherov", "TBL", 37, 84),
            Player("Connor McDavid", "EDM", 26, 74),
            Player("Leon Draisaitl", "EDM", 52, 54),
        ]


class TestStatisticsService(unittest.TestCase):
    def test_search(self):
        service = StatisticsService(StubPlayerReader())
        result = service.search("Kucherov")
        self.assertEqual(result.name, "Nikita Kucherov")

    def test_search_wrong_name(self):
        service = StatisticsService(StubPlayerReader())
        result = service.search("Miau")
        self.assertIsNone(result)

    def test_team(self):
        service = StatisticsService(StubPlayerReader())
        result = service.team("EDM")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Connor McDavid")
        self.assertEqual(result[1].name, "Leon Draisaitl")

    def test_wrong_team(self):
        service = StatisticsService(StubPlayerReader())
        result = service.team("MIAU")
        self.assertEqual(result, [])

    def test_top_in_point_order(self):
        service = StatisticsService(StubPlayerReader())
        result = service.top(2)
        self.assertEqual(result[0].name, "Nikita Kucherov")
        self.assertEqual(result[1].name, "Leon Draisaitl")
