import json
import math
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager
from pathlib import Path
from time import perf_counter


def generate_dataset(size):
    return [
        ((index * 17) % 1000) + (index % 13)
        for index in range(size)
    ]


def chunk_data(data, chunk_size):
    return [
        data[index:index + chunk_size]
        for index in range(0, len(data), chunk_size)
    ]


def count_primes(numbers):
    def is_prime(value):
        if value < 2:
            return False
        if value == 2:
            return True
        if value % 2 == 0:
            return False

        limit = int(math.sqrt(value)) + 1
        for factor in range(3, limit, 2):
            if value % factor == 0:
                return False
        return True

    return sum(1 for number in numbers if is_prime(number))


def process_chunk(chunk_index, values, fail_chunk_indices):
    if chunk_index in fail_chunk_indices:
        raise RuntimeError(f"Simulated worker failure at chunk {chunk_index}")

    total = sum(values)
    count = len(values)
    mean = total / count
    variance = sum((value - mean) ** 2 for value in values) / count
    prime_count = count_primes(values)

    return {
        "chunk_index": chunk_index,
        "count": count,
        "sum": total,
        "mean": mean,
        "variance": variance,
        "prime_count": prime_count,
        "min": min(values),
        "max": max(values),
    }


def combine_results(chunk_results):
    total_count = sum(item["count"] for item in chunk_results)
    total_sum = sum(item["sum"] for item in chunk_results)
    weighted_variance_sum = sum(item["variance"] * item["count"] for item in chunk_results)

    if total_count == 0:
        return {
            "processed_chunks": 0,
            "total_count": 0,
            "total_sum": 0,
            "global_mean": None,
            "global_variance": None,
            "total_prime_count": 0,
            "global_min": None,
            "global_max": None,
        }

    return {
        "processed_chunks": len(chunk_results),
        "total_count": total_count,
        "total_sum": total_sum,
        "global_mean": total_sum / total_count,
        "global_variance": weighted_variance_sum / total_count,
        "total_prime_count": sum(item["prime_count"] for item in chunk_results),
        "global_min": min(item["min"] for item in chunk_results),
        "global_max": max(item["max"] for item in chunk_results),
    }


def main():
    config_path = Path(__file__).with_name("config.json")
    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    dataset = generate_dataset(config["dataset_size"])
    chunks = chunk_data(dataset, config["chunk_size"])
    total_chunks = len(chunks)

    fail_chunk_indices = set(config.get("fail_chunk_indices", []))
    if not config.get("simulate_worker_failures", False):
        fail_chunk_indices = set()

    output_path = config_path.parent / config["output_file"]
    error_path = config_path.parent / config["error_log_file"]

    start = perf_counter()

    with Manager() as manager:
        progress_state = manager.dict({"completed": 0, "failed": 0})
        chunk_results = []
        failures = []

        with ProcessPoolExecutor(max_workers=config["max_workers"]) as executor:
            futures = {
                executor.submit(process_chunk, chunk_index, values, fail_chunk_indices): chunk_index
                for chunk_index, values in enumerate(chunks)
            }

            for future in as_completed(futures):
                chunk_index = futures[future]
                try:
                    result = future.result()
                    chunk_results.append(result)
                except Exception as exc:
                    failures.append(
                        {
                            "chunk_index": chunk_index,
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
                    progress_state["failed"] = progress_state["failed"] + 1
                finally:
                    progress_state["completed"] = progress_state["completed"] + 1
                    print(
                        f"Progress: {progress_state['completed']}/{total_chunks} chunks "
                        f"(failed: {progress_state['failed']})"
                    )

        chunk_results.sort(key=lambda item: item["chunk_index"])
        combined = combine_results(chunk_results)

        output_payload = {
            "configuration": config,
            "dataset_size": len(dataset),
            "total_chunks": total_chunks,
            "successful_chunks": len(chunk_results),
            "failed_chunks": len(failures),
            "combined_result": combined,
            "chunk_results": chunk_results,
            "elapsed_seconds": round(perf_counter() - start, 4),
            "worker_count": config["max_workers"],
            "host_cpu_count": os.cpu_count(),
        }

        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(output_payload, output_file, indent=2)

        with error_path.open("w", encoding="utf-8") as error_file:
            for failure in failures:
                error_file.write(json.dumps(failure) + "\n")

    print("Processing complete.")
    print(f"Successful chunks: {len(chunk_results)}")
    print(f"Failed chunks: {len(failures)}")
    print(f"Results written to: {output_path.name}")
    print(f"Errors written to: {error_path.name}")


if __name__ == "__main__":
    main()
