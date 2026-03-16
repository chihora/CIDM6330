import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen

lock = threading.Lock()

def fetch_url(url, timeout):
    try:
        with urlopen(url, timeout=timeout) as response:
            data = response.read().decode("utf-8")
            return {"url": url, "data": data}
    except Exception as e:
        return {"url": url, "error": str(e)}

def main():
    with open("config.json") as f:
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

    with open(config["output_file"], "w") as f:
        json.dump(results, f, indent=2)

    with open(config["error_log_file"], "w") as f:
        for error in errors:
            f.write(str(error) + "\n")

    print("Fetching complete.")
    print("Results saved to results.json")
    print("Errors saved to errors.log")

if __name__ == "__main__":
    main()