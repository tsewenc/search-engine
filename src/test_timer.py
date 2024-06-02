import time

class Timer:
    def __init__(self, text="Elapsed time") -> None:
        self.text = text

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start
        print(f"{self.text}: {self.interval:.4f} seconds")