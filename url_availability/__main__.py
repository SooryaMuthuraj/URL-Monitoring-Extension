import threading
import time
import requests
from dynatrace_extension import Extension, Status, StatusValue


class URLChecker(threading.Thread):
    def __init__(self, extension, endpoint):
        super().__init__(daemon=True)
        self.extension = extension
        self.url = endpoint.get("url")
        self.timeout = int(endpoint.get("timeout", 5))
        self.interval = int(endpoint.get("schedule_interval", 1)) * 60

        ssl_value = str(endpoint.get("ssl_enable", "true")).strip().lower()
        self.ssl_enable = False if ssl_value == "false" else True

        self._stop_event = threading.Event()
        self._lock = threading.Lock()

    def run(self):
        while not self._stop_event.is_set():
            with self._lock:
                availability = 0
                response_code = 0
                response_time_ms = 0

                try:
                    start = time.time()
                    response = requests.get(
                        self.url,
                        timeout=self.timeout,
                        verify=self.ssl_enable
                    )
                    response_time_ms = int((time.time() - start) * 1000)

                    response_code = response.status_code
                    availability = 1 if response.ok else 0

                except requests.exceptions.SSLError as e:
                    self.extension.logger.error(
                        f"SSL error for {self.url} (ssl_enable={self.ssl_enable}): {e}"
                    )

                except requests.exceptions.RequestException as e:
                    self.extension.logger.error(
                        f"URL check failed for {self.url}: {e}"
                    )

                dimensions = {"url": self.url}

                self.extension.report_metric(
                    "custom.url.availability",
                    availability,
                    dimensions=dimensions
                )

                self.extension.report_metric(
                    "custom.url.response_code",
                    response_code,
                    dimensions=dimensions
                )

                self.extension.report_metric(
                    "custom.url.response_time",
                    response_time_ms,
                    dimensions=dimensions
                )

                self.extension.logger.info(
                    f"URL check: {self.url} | "
                    f"availability={availability}, "
                    f"code={response_code}, "
                    f"time={response_time_ms}ms, "
                    f"ssl_verify={self.ssl_enable}"
                )

            for _ in range(self.interval):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def stop(self):
        self._stop_event.set()


class ExtensionImpl(Extension):
    def __init__(self, name):
        super().__init__(name)
        self.checkers = {}

    def query(self):
        endpoints = self.activation_config.get("endpoints", [])

        for endpoint in endpoints:
            url = endpoint.get("url")
            if url not in self.checkers or not self.checkers[url].is_alive():
                checker = URLChecker(self, endpoint)
                self.checkers[url] = checker
                checker.start()

    def fastcheck(self):
        return Status(StatusValue.OK)

    def shutdown(self):
        for checker in self.checkers.values():
            checker.stop()
        super().shutdown()


def main():
    ext = ExtensionImpl(name="url_availability")
    ext.run()


if __name__ == "__main__":
    main()




# import threading
# import time
# import logging
# import requests
# from dynatrace_extension import Extension, Status, StatusValue


# class URLChecker(threading.Thread):
#     def __init__(self, extension, endpoint):
#         super().__init__(daemon=True)
#         self.extension = extension
#         self.url = endpoint.get("url")
#         self.timeout = int(endpoint.get("timeout", 5))
#         self.interval = int(endpoint.get("schedule_interval", 1)) * 60
#         self._stop_event = threading.Event()
#         self._lock = threading.Lock()

#     def run(self):
#         while not self._stop_event.is_set():
#             with self._lock:
#                 availability = 0
#                 response_code = 0
#                 response_time_ms = 0

#                 try:
#                     start = time.time()
#                     response = requests.get(self.url, timeout=self.timeout)
#                     response_time_ms = int((time.time() - start) * 1000)

#                     response_code = response.status_code
#                     availability = 1 if response.ok else 0

#                 except requests.exceptions.RequestException as e:
#                     self.extension.logger.error(f"URL check failed for {self.url}: {e}")

#                 dimensions = {"url": self.url}

#                 self.extension.report_metric(
#                     "custom.url.availability",
#                     availability,
#                     dimensions=dimensions
#                 )

#                 self.extension.report_metric(
#                     "custom.url.response_code",
#                     response_code,
#                     dimensions=dimensions
#                 )

#                 self.extension.report_metric(
#                     "custom.url.response_time",
#                     response_time_ms,
#                     dimensions=dimensions
#                 )

#                 self.extension.logger.info(
#                     f"URL check: {self.url} | "
#                     f"availability={availability}, "
#                     f"code={response_code}, "
#                     f"time={response_time_ms}ms"
#                 )

#             for _ in range(self.interval):
#                 if self._stop_event.is_set():
#                     break
#                 time.sleep(1)

#     def stop(self):
#         self._stop_event.set()


# class ExtensionImpl(Extension):
#     def __init__(self, name):
#         super().__init__(name)
#         self.checkers = {}

#     def query(self):
#         self.logger.info("Starting URL checks...")
#         endpoints = self.activation_config.get("endpoints", [])

#         for endpoint in endpoints:
#             url = endpoint.get("url")
#             if url not in self.checkers or not self.checkers[url].is_alive():
#                 checker = URLChecker(self, endpoint)
#                 self.checkers[url] = checker
#                 checker.start()

#         self.logger.info("All URL checkers started.")

#     def fastcheck(self):
#         return Status(StatusValue.OK)

#     def shutdown(self):
#         for checker in self.checkers.values():
#             checker.stop()
#         super().shutdown()


# def main():
#     ext = ExtensionImpl(name="url_availability")
#     try:
#         ext.run()
#     except KeyboardInterrupt:
#         ext.shutdown()


# if __name__ == "__main__":
#     main()
