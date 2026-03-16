import subprocess
import sys
import time
from pathlib import Path


def run_script(script_name):
    script_path = Path(__file__).with_name(script_name)
    start = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, str(script_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    elapsed = time.perf_counter() - start
    return completed.returncode, elapsed, completed.stdout, completed.stderr


def print_result(name, return_code, elapsed, stdout, stderr):
    status = "OK" if return_code == 0 else "FAILED"
    print(f"[{name}] {status} in {elapsed:.3f}s")
    if stdout.strip():
        print(stdout.strip())
    if stderr.strip():
        print(stderr.strip())


def main():
    threaded_result = run_script("fetch_data.py")
    asyncio_result = run_script("fetch_data_async.py")

    print_result("ThreadPoolExecutor", *threaded_result)
    print()
    print_result("Asyncio (aiohttp)", *asyncio_result)

    threaded_elapsed = threaded_result[1]
    asyncio_elapsed = asyncio_result[1]

    if threaded_result[0] == 0 and asyncio_result[0] == 0:
        diff = threaded_elapsed - asyncio_elapsed
        if diff > 0:
            print(f"\nAsyncio was faster by {diff:.3f}s")
        elif diff < 0:
            print(f"\nThreaded version was faster by {abs(diff):.3f}s")
        else:
            print("\nBoth implementations took the same time.")
    else:
        print("\nAt least one run failed; speed comparison skipped.")


if __name__ == "__main__":
    main()
