import unittest
from model.data_model import CompetitionModel
from unittest.mock import MagicMock

class TestCompetitionModel(unittest.TestCase):
    def test_get_competition_names(self):
        mock_client = MagicMock()
        mock_client.get_competitions.return_value = {
            "competitions": [{"name": "Premier League"}, {"name": "La Liga"}]
        }

        model = CompetitionModel(mock_client)
        names = model.get_competition_names()
        self.assertEqual(names, ["Premier League", "La Liga"])
