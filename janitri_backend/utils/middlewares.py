import time

class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        duration = (time.perf_counter() - start_time) * 1000  # in ms
        response["X-Response-Time-ms"] = f"{duration:.2f}"
        return response
