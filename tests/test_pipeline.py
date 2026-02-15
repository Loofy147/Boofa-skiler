import unittest
from unittest.mock import patch, MagicMock
from layers.layer_3_optimization.pipeline import BoofaSkiler

class TestBoofaSkiler(unittest.TestCase):
    def setUp(self):
        self.k_token = "test_kaggle_token"
        self.h_token = "test_hf_token"
        self.skiler = BoofaSkiler(self.k_token, self.h_token)

    def test_initial_q_score(self):
        self.assertEqual(self.skiler.q_score, 0.761)

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('os.chmod')
    def test_configure_environment(self, mock_chmod, mock_open, mock_makedirs):
        success = self.skiler.configure_environment()
        self.assertTrue(success)
        mock_makedirs.assert_called()
        mock_open.assert_called()

    @patch('subprocess.run')
    def test_fetch_kaggle_competitions_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="comp1\ncomp2\ncomp3\ncomp4\ncomp5\ncomp6")
        result = self.skiler.fetch_kaggle_competitions(limit=2)
        self.assertIsNotNone(result)
        # Check if it contains the header and 2 competitions
        self.assertEqual(len(result.splitlines()), 4)

    @patch('layers.layer_3_optimization.pipeline.model_info')
    def test_get_hf_model_details(self, mock_model_info):
        mock_info = MagicMock()
        mock_info.modelId = "test-model"
        mock_info.tags = ["tag1"]
        mock_info.downloads = 100
        mock_info.likes = 10
        mock_model_info.return_value = mock_info
        
        details = self.skiler.get_hf_model_details("test-model")
        self.assertEqual(details["id"], "test-model")
        self.assertEqual(details["downloads"], 100)

    def test_calculate_optimized_q_score(self):
        score = self.skiler.calculate_optimized_q_score()
        self.assertEqual(score, 0.9205)
        self.assertEqual(self.skiler.q_score, 0.9205)

if __name__ == "__main__":
    unittest.main()
