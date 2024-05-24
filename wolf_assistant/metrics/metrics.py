from prometheus_client import Counter, Histogram


# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')
CURRENT_USERS = Counter('current_users', 'Current number of users')

AUDIO_REQUEST_COUNT = Counter('audio_request_count', 'Number of audio requests')
IMAGE_REQUEST_COUNT = Counter('image_request_count', 'Number of image requests')
VIDEO_REQUEST_COUNT = Counter('video_request_count', 'Number of video requests')