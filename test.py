import subprocess
import threading
import time

def check_playerctl(player):
    try:
        output = subprocess.check_output([f'playerctl status --player="{player}"'], shell=True)

        if b"Playing" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        return False


def run_thread(thread_id, stop_event, player):
    """Runs a single thread that checks playerctl output."""
    while not stop_event.is_set():
        result = check_playerctl(player)
        if result == 1:
            print(f"Thread {thread_id}: Condition met. Stopping all threads.")
            stop_event.set()  # Signal to stop other threads
            break  # Exit this thread
        time.sleep(1)  # Adjust the sleep time as needed.


def multithreaded_playerctl_check():
    """Runs three threads concurrently to check playerctl output."""
    stop_event = threading.Event()
    threads = []

    players = str(subprocess.check_output(['playerctl', '-l'], text=True))[:-1].split('\n')

    for i,player in enumerate(players):
        thread = threading.Thread(target=run_thread, args=(i + 1, stop_event, player))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    multithreaded_playerctl_check()
