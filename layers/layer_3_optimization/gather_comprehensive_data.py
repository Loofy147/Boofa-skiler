import os
import json
import subprocess
import logging
from typing import List, Dict, Any
from huggingface_hub import HfApi, list_datasets, list_models
from layers.layer_2_core.realization_engine import RealizationFeatures

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataGatherer:
    def __init__(self, kaggle_token: str, hf_token: str):
        self.kaggle_token = kaggle_token
        self.hf_token = hf_token
        self.api_hf = HfApi(token=hf_token)

    def fetch_kaggle_datasets(self, query: str, limit: int = 10) -> List[Dict]:
        try:
            logger.info(f"Searching Kaggle datasets for: {query}")
            result = subprocess.run(
                ["kaggle", "datasets", "list", "-s", query],
                capture_output=True, text=True, check=True
            )
            lines = result.stdout.splitlines()
            if len(lines) < 3: return []

            datasets = []
            # Skip header and separator
            for line in lines[2:limit+2]:
                parts = line.split()
                if len(parts) >= 2:
                    datasets.append({
                        "ref": parts[0],
                        "title": " ".join(parts[1:min(len(parts), 5)]),
                        "topic": query
                    })
            return datasets
        except Exception as e:
            logger.error(f"Kaggle Dataset search failed: {e}")
            return []

    def fetch_hf_trending(self, limit: int = 10) -> List[Dict]:
        try:
            logger.info("Fetching trending Hugging Face datasets...")
            datasets = list_datasets(sort="downloads", direction=-1, limit=limit, token=self.hf_token)
            return [{"id": d.id, "downloads": getattr(d, 'downloads', 0), "tags": d.tags} for d in datasets]
        except Exception as e:
            logger.error(f"HF Dataset fetch failed: {e}")
            return []

    def convert_to_realizations(self, data_list: List[Dict], source: str) -> List[Dict]:
        realizations = []
        for item in data_list:
            content = ""
            if source == "Kaggle":
                content = f"Kaggle Dataset '{item.get('title', 'N/A')}' (ref: {item.get('ref', 'N/A')}) offers potential features for {item.get('topic', 'general')} optimization."
            else:
                content = f"HF Dataset '{item.get('id', 'N/A')}' is a high-impact data source with {item.get('downloads', 0)} downloads, enhancing system grounding."

            # Generate deterministic-ish features based on downloads/popularity
            popularity = min(item.get('downloads', 500) / 10000.0, 1.0) if source == "HF" else 0.8
            features = {
                "grounding": 0.85 + (popularity * 0.1),
                "certainty": 0.90,
                "structure": 0.80,
                "applicability": 0.95,
                "coherence": 0.90,
                "generativity": 0.70 + (popularity * 0.2)
            }
            realizations.append({
                "content": content,
                "features": features,
                "source": source,
                "id": item.get('ref') or item.get('id')
            })
        return realizations

def _get_default_mock_data():
    """Provides minimal but valid mock data structure if file is missing."""
    return [
        {
            "content": "Kaggle Dataset 'AI Mathematical Olympiad' offers potential features for reasoning optimization.",
            "features": {"grounding": 0.9, "certainty": 0.9, "structure": 0.85, "applicability": 0.95, "coherence": 0.9, "generativity": 0.8},
            "source": "Kaggle", "id": "aimo-3"
        },
        {
            "content": "HF Dataset 'MiniMaxAI/MiniMax-M2.5' is a high-impact data source enhancing system grounding.",
            "features": {"grounding": 0.95, "certainty": 0.92, "structure": 0.9, "applicability": 0.98, "coherence": 0.95, "generativity": 0.9},
            "source": "HF", "id": "minimax"
        }
    ]

def gather_all():
    k_token = os.getenv("KAGGLE_API_TOKEN")
    h_token = os.getenv("HF_TOKEN")

    if not k_token or not h_token:
        logger.error("Tokens missing")
        return []

    if k_token == "DUMMY" or h_token == "DUMMY":
        logger.warning("Running gather_all in MOCK mode due to DUMMY tokens.")
        mock_data_path = "data/comprehensive_external_data.json"

        if os.path.exists(mock_data_path):
            try:
                with open(mock_data_path, "r") as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} records from mock data file")
                    return data
            except Exception as e:
                logger.error(f"Failed to parse mock data file: {e}")
                return _get_default_mock_data()
        else:
            logger.warning(f"Mock data file not found at {mock_data_path}, using default mock data")
            return _get_default_mock_data()

    gatherer = DataGatherer(k_token, h_token)

    # Gather from Kaggle
    kaggle_data = []
    for q in ["reasoning", "strategic", "mathematics"]:
        kaggle_data.extend(gatherer.fetch_kaggle_datasets(q, limit=5))

    # Gather from HF
    hf_data = gatherer.fetch_hf_trending(limit=10)

    all_realizations = gatherer.convert_to_realizations(kaggle_data, "Kaggle")
    all_realizations.extend(gatherer.convert_to_realizations(hf_data, "HF"))

    os.makedirs("data", exist_ok=True)
    with open("data/comprehensive_external_data.json", "w") as f:
        json.dump(all_realizations, f, indent=2)

    logger.info(f"Gathered {len(all_realizations)} comprehensive realizations.")
    return all_realizations

if __name__ == "__main__":
    gather_all()
