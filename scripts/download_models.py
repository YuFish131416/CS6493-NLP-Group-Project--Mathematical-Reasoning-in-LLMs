"""
Download GGUF model files from HuggingFace Hub.
Run this script to download the required models for the experiment.

Usage:
    python scripts/download_models.py
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def download_models():
    from huggingface_hub import hf_hub_download

    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    os.makedirs(models_dir, exist_ok=True)

    downloads = [
        {
            "repo_id": "QuantFactory/Qwen2.5-Math-1.5B-Instruct-GGUF",
            "filename": "Qwen2.5-Math-1.5B-Instruct.Q4_K_M.gguf",
            "local_name": "qwen2.5-math-1.5b-q4_k_m.gguf",
        },
        {
            "repo_id": "bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF",
            "filename": "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf",
            "local_name": "deepseek-r1-qwen-1.5b-q4_k_m.gguf",
        },
    ]

    for model in downloads:
        target_path = os.path.join(models_dir, model["local_name"])
        if os.path.exists(target_path):
            size_mb = os.path.getsize(target_path) / (1024 * 1024)
            print(f"[SKIP] {model['local_name']} already exists ({size_mb:.0f} MB)")
            continue

        print(f"[DOWNLOADING] {model['repo_id']} / {model['filename']}...")
        try:
            downloaded_path = hf_hub_download(
                repo_id=model["repo_id"],
                filename=model["filename"],
                local_dir=models_dir,
                local_dir_use_symlinks=False,
            )
            # Rename to our expected name
            actual_downloaded = os.path.join(models_dir, model["filename"])
            if os.path.exists(actual_downloaded) and actual_downloaded != target_path:
                os.rename(actual_downloaded, target_path)
            elif os.path.exists(downloaded_path) and downloaded_path != target_path:
                import shutil
                shutil.copy2(downloaded_path, target_path)

            size_mb = os.path.getsize(target_path) / (1024 * 1024)
            print(f"[DONE] {model['local_name']} ({size_mb:.0f} MB)")
        except Exception as e:
            print(f"[ERROR] Failed to download {model['local_name']}: {e}")
            raise

    print("\nAll models downloaded successfully!")
    print(f"Models directory: {models_dir}")
    for f in os.listdir(models_dir):
        if f.endswith('.gguf'):
            size = os.path.getsize(os.path.join(models_dir, f)) / (1024 * 1024)
            print(f"  - {f} ({size:.0f} MB)")


if __name__ == "__main__":
    download_models()
