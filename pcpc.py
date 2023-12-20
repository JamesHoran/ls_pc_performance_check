import psutil
import time
from tqdm import tqdm

def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        print(f"Error retrieving CPU usage: {e}")
        return None

def get_memory_usage():
    try:
        return psutil.virtual_memory().percent
    except Exception as e:
        print(f"Error retrieving memory usage: {e}")
        return None

def get_physical_memory_usage():
    try:
        return psutil.virtual_memory().percent - psutil.swap_memory().percent
    except Exception as e:
        print(f"Error retrieving physical memory usage: {e}")
        return None

def get_swap_memory_usage():
    try:
        return psutil.swap_memory().percent
    except Exception as e:
        print(f"Error retrieving swap memory usage: {e}")
        return None

def get_disk_usage():
    try:
        return psutil.disk_usage('/').percent
    except Exception as e:
        print(f"Error retrieving disk usage: {e}")
        return None

def analyze_performance(cpu_usage, memory_usage, swap_usage, disk_usage):
    issues = set()  # Using a set to ensure uniqueness

    if cpu_usage is None or memory_usage is None or swap_usage is None or disk_usage is None:
        return {"Error: Unable to retrieve system information."}

    if cpu_usage > 80:
        issues.add("High CPU usage may be causing slowness.")
    if memory_usage > 80:
        issues.add("High memory usage may be causing slowness.")
    if get_physical_memory_usage() > 80:
        issues.add("High physical memory usage may be causing slowness.")
    if swap_usage > 80:
        issues.add("High swap memory usage may be causing slowness.")
    if disk_usage > 80:
        issues.add("High disk usage may be causing slowness.")

    return issues if issues else {"None"}

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}m {int(seconds)}s"

def main():
    print("---------- Start of Script ----------")

    duration = 3600  # Set the duration of the script in seconds
    issues_detected = set()  # Using a set to ensure uniqueness

    for remaining_time in tqdm(range(duration), desc="Progress"):
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        swap_usage = get_swap_memory_usage()
        disk_usage = get_disk_usage()

        detected_issues = analyze_performance(cpu_usage, memory_usage, swap_usage, disk_usage)
        issues_detected.update(detected_issues)

        tqdm.write(f"Time left: {format_time(duration - remaining_time)}", end="\r")

        time.sleep(1)  # Sleep for 1 second before the next iteration

    print("\nFinal Report:")
    print(f"Issues: {' | '.join(issues_detected)}")

    print("---------- End of Script ----------")

if __name__ == "__main__":
    main()

