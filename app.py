from prometheus_client import start_http_server, Gauge
import requests
import time

# Define metrics for URL status and response time
url_up = Gauge('sample_external_url_up', 'Indicates if the external URL is up (1 for up, 0 for down)', ['url'])
url_response_ms = Gauge('sample_external_url_response_ms', 'Response time of the external URL in milliseconds', ['url'])

# URLs to monitor
urls = ["https://httpstat.us/503", "https://httpstat.us/200"]

def check_url(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)  # timeout to avoid hanging
        elapsed_time_ms = (time.time() - start_time) * 1000  # convert to ms
        if response.status_code == 200:
            url_up.labels(url=url).set(1)
        else:
            url_up.labels(url=url).set(0)
        url_response_ms.labels(url=url).set(elapsed_time_ms)
    except Exception as e:
        # On exception, mark URL as down and set response time to 0
        url_up.labels(url=url).set(0)
        url_response_ms.labels(url=url).set(0)
        print(f"Error checking {url}: {e}")

if __name__ == '__main__':
    # Start up the server to expose the metrics on port 8000.
    start_http_server(8000)
    print("Prometheus metrics server started on port 8000")
    # Loop forever to update metrics every 10 seconds.
    while True:
        for url in urls:
            check_url(url)
        time.sleep(10)
