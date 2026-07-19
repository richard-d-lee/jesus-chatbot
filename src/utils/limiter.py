from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Shared limiter instance; initialized against the app in main.py.
# In-memory storage is fine for a single-instance deployment.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)
