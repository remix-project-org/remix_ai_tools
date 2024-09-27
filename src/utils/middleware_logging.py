import os, csv, json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
from time import time
from datetime import datetime

# handle profiling
PROFIL_FILE = "profile.csv"

if not os.path.exists(PROFIL_FILE):
    with open(PROFIL_FILE, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "endpoint", "method", "total_request_time", "llm_duration", "llm_average_duration"])


class GradioProfilingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time

        # deep copy the response to avoid consuming the original response
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        try:
            data = json.loads(response_body.decode('utf-8'))
            duration = data.get("duration", 0)
            average_duration = data.get("average_duration", 0)
        except:
            duration = 0
            average_duration = 0

        # Check if the request is to a internal Gradio endpoint and log into file
        print(f"Request: {request.method} {request.url.path} took {process_time:.4f} seconds")
        log_entry = [datetime.now().isoformat(), request.url.path, request.method, "{time:.3f}".format(time=process_time),  "{dur:.3f}".format(dur=duration),  "{avg_dur:.3f}".format(avg_dur=average_duration)]
        with open(PROFIL_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(log_entry)
            

        return Response(
            content=response_body,  # Reusing the captured body
            status_code=response.status_code,  # Preserving original status code
            headers=dict(response.headers),  # Preserving original headers
            media_type=response.media_type  # Preserving the original media type
        )
