import os
import multiprocessing

# Bind to the port Render provides
port = os.environ.get('PORT', '10000')
bind = f"0.0.0.0:{port}"

# Use sync workers for Flask (WSGI)
workers = 1  # Start with 1 worker for free tier
worker_class = "sync"

# Timeout settings
timeout = 120
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload app for better performance
preload_app = True

# Worker processes
max_requests = 1000
max_requests_jitter = 100
