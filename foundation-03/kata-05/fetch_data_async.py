import asyncio
import json
from pathlib import Path

import aiohttp


def build_async_output_path(config_path, output_name):
    output_path = Path(output_name)
    if not output_path.is_absolute():
        output_path = config_path.parent / output_path

    return output_path.with_name(f"{output_path.stem}_async{output_path.suffix}")


async def fetch_url(session, url, timeout_seconds, semaphore):
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_seconds)
            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                data = await response.json()
                return {"url": url, "data": data}
        except Exception as exc:
            return {"url": url, "error": f"{type(exc).__name__}: {exc}"}


async def run_async_fetch(config):
    urls = config["urls"]
    pool_size = config["thread_pool_size"]
    timeout_seconds = config["timeout_seconds"]

    semaphore = asyncio.Semaphore(pool_size)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, timeout_seconds, semaphore) for url in urls]
        completed = await asyncio.gather(*tasks)

    results = [item for item in completed if "data" in item]
    errors = [item for item in completed if "error" in item]

    return results, errors


def main():
    config_path = Path(__file__).with_name("config.json")
    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    results, errors = asyncio.run(run_async_fetch(config))

    output_file = build_async_output_path(config_path, config["output_file"])
    error_file = build_async_output_path(config_path, config["error_log_file"])

    with output_file.open("w", encoding="utf-8") as out_file:
        json.dump(results, out_file, indent=2)

    with error_file.open("w", encoding="utf-8") as err_file:
        for error in errors:
            err_file.write(str(error) + "\n")

    print(f"Completed fetching {len(config['urls'])} URL(s) with asyncio.")
    print(f"Successful fetches: {len(results)}")
    print(f"Failed fetches: {len(errors)}")
    print(f"Results written to: {output_file.name}")
    print(f"Errors written to: {error_file.name}")


if __name__ == "__main__":
    main()
