import threading
import time


def do_work():
    time.sleep(1)
    print('Done')


def run():
    threads = []

    for _ in range(5):
        t = threading.Thread(target=do_work)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


start_time = time.perf_counter()
run()
end_time = time.perf_counter()
print(f"{end_time - start_time:.20f}")
