import json
import subprocess
import sys
from pathlib import Path


def expected_total_count(config, total_chunks):
    chunk_size = config["chunk_size"]
    dataset_size = config["dataset_size"]

    failed = set(config.get("fail_chunk_indices", [])) if config.get("simulate_worker_failures", False) else set()

    expected = 0
    for chunk_index in range(total_chunks):
        if chunk_index in failed:
            continue

        start = chunk_index * chunk_size
        remaining = max(dataset_size - start, 0)
        expected += min(chunk_size, remaining)

    return expected


def main():
    script_dir = Path(__file__).resolve().parent
    process_script = script_dir / "process_data.py"
    config_path = script_dir / "config.json"
    output_path = script_dir / "results.json"

    run = subprocess.run([sys.executable, str(process_script)], cwd=script_dir)
    if run.returncode != 0:
        print("process_data.py failed")
        sys.exit(1)

    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    with output_path.open("r", encoding="utf-8") as output_file:
        results = json.load(output_file)

    total_chunks = results["total_chunks"]
    actual_total_count = results["combined_result"]["total_count"]
    expected_count = expected_total_count(config, total_chunks)

    if actual_total_count != expected_count:
        print(
            "Validation failed: expected total_count "
            f"{expected_count}, got {actual_total_count}"
        )
        sys.exit(1)

    print("Validation passed")


if __name__ == "__main__":
    main()
