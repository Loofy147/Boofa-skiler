import os
from huggingface_hub import HfApi
import kaggle

def setup_medgemma():
    print("🚀 Setting up MedGemma Impact Challenge Environment...")

    # 1. Hugging Face Check
    print("\n[1] Hugging Face Discovery")
    api = HfApi()
    try:
        models = api.list_models(search='MedGemma')
        print("✅ MedGemma Models found on Hub:")
        for m in list(models)[:5]:
            print(f"  - {m.modelId}")
    except Exception as e:
        print(f"⚠️ Error accessing Hugging Face Hub: {e}")
        print("Note: HF_TOKEN may be required for gated models.")

    # 2. Kaggle Check
    print("\n[2] Kaggle Competition Discovery")
    try:
        # We use os.environ['KAGGLE_API_TOKEN'] but the kaggle-py library
        # usually expects a kaggle.json file or specific env vars.
        # Since we use the CLI wrapper, we can just check if it's set.
        if 'KAGGLE_API_TOKEN' in os.environ:
             print("✅ KAGGLE_API_TOKEN is set.")
        else:
             print("⚠️ KAGGLE_API_TOKEN is NOT set.")
    except Exception as e:
        print(f"⚠️ Error checking Kaggle: {e}")

    print("\n✨ Setup check complete.")

if __name__ == "__main__":
    setup_medgemma()
