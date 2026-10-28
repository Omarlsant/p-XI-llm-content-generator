import time
import asyncio
from collections import defaultdict
from fastapi import Request, HTTPException
from core.config import settings
from core.log_config import logger

class InMemoryRateLimiter:
    """
    Thread-safe, sliding-window in-memory rate limiter per client IP.
    Applies rate limits to incoming requests.
    """
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self._records = defaultdict(list)
        self._lock = asyncio.Lock()

    def is_allowed(self, client_ip: str) -> bool:
        """Check if request from client IP is allowed within the rate limit window."""
        rpm = getattr(settings, "RATE_LIMIT_PER_MINUTE", self.requests_per_minute)
        if rpm <= 0:
            return True
        now = time.time()
        history = self._records[client_ip]
        valid_history = [t for t in history if now - t < self.window_seconds]
        if len(valid_history) >= rpm:
            self._records[client_ip] = valid_history
            return False
        valid_history.append(now)
        self._records[client_ip] = valid_history
        return True

    def get_retry_after(self, client_ip: str) -> int:
        """Calculate seconds until client can retry after being rate limited."""
        now = time.time()
        history = self._records.get(client_ip, [])
        valid_history = [t for t in history if now - t < self.window_seconds]
        if not valid_history:
            return 0
        oldest = valid_history[0]
        return max(1, int(self.window_seconds - (now - oldest)))

    async def __call__(self, request: Request):
        # Only rate limit mutating/expensive operations (POST requests)
        if request.method != "POST":
            return

        rpm = getattr(settings, "RATE_LIMIT_PER_MINUTE", self.requests_per_minute)
        if rpm <= 0:
            return  # Rate limiting disabled

        client_ip = request.client.host if request.client else "unknown"

        async with self._lock:
            if not self.is_allowed(client_ip):
                retry_after = self.get_retry_after(client_ip)
                logger.warning(
                    f"Rate limit exceeded for client IP: {client_ip} "
                    f"({len(self._records[client_ip])} requests in 60s window, max {rpm})"
                )
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded: maximum {rpm} requests per minute allowed.",
                    headers={"Retry-After": str(retry_after)}
                )

# Singleton instance for dependency injection
rate_limiter = InMemoryRateLimiter(settings.RATE_LIMIT_PER_MINUTE)
