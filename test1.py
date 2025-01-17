import threading
import time
import subprocess

def print_letters(text, stop_event):
    """Prints letters from the string with a 1-second delay."""
    for char in text:
        if stop_event.is_set():
            break
        print(char)
        time.sleep(1)

def check_cmus(stop_event):
    """Checks if csoundis playing and stops the functions if it is."""
    while not stop_event.is_set():
        try:
            output = subprocess.check_output(['cmus-remote', '--query'], text=True)  #Error handling later.
            if "status playing" in output:  #Check csoundoutput for "status playing"
                print("csoundis playing. Stopping functions.")
                stop_event.set()  # Signal to stop other functions
                break
        except subprocess.CalledProcessError:
             print("cmus-remote not found or error running command")
             stop_event.set() #If something goes wrong, stop.
             break
        except FileNotFoundError:
            print("cmus-remote not found.")
            stop_event.set()
            break
        time.sleep(1)  # Check every second


if __name__ == "__main__":
    my_string = "abcdefghijklmnopqrstuvwxyz"
    stop_event = threading.Event()

    thread1 = threading.Thread(target=print_letters, args=(my_string, stop_event))
    thread2 = threading.Thread(target=check_cmus, args=(stop_event,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Both functions finished.")
