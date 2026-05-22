import threading

def run_threads(tasks):
    threads = []

    for task in tasks:
        t = threading.Thread(target=task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
