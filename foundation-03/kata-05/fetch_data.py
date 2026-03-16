import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen
from pathlib import Path

lock = threading.Lock()


def fetch_url(url, timeout):
    try:
        with urlopen(url, timeout=timeout) as response:
            data = response.read().decode("utf-8")
            parsed_data = json.loads(data)
            return {"url": url, "data": parsed_data}
    except Exception as e:
        return {"url": url, "error": f"{type(e).__name__}: {e}"}


def main():
    config_path = Path(__file__).with_name("config.json")
    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    urls = config["urls"]
    thread_pool_size = config["thread_pool_size"]
    timeout = config["timeout_seconds"]

    results = []
    errors = []

    with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
        futures = [executor.submit(fetch_url, url, timeout) for url in urls]

        for future in as_completed(futures):
            result = future.result()

            with lock:
                if "error" in result:
                    errors.append(result)
                else:
                    results.append(result)

    with open(config["output_file"], "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open(config["error_log_file"], "w", encoding="utf-8") as f:
        for error in errors:
            f.write(str(error) + "\n")

    print(f"Completed fetching {len(urls)} URL(s).")
    print(f"Successful fetches: {len(results)}")
    print(f"Failed fetches: {len(errors)}")
    print(f"Results written to: {config['output_file']}")
    print(f"Errors written to: {config['error_log_file']}")


if __name__ == "__main__":
    main()