import asyncio
import time


class RateLimiter:
    """
    Limiteur de débit asynchrone : garantit un intervalle minimal entre deux
    requêtes, même si de nombreuses tâches l'appellent en parallèle.
    """
    def __init__(self, min_interval: float) -> None:
        self.min_interval = min_interval
        self._lock = asyncio.Lock()
        self._next_allowed = 0.0

    async def wait(self) -> None:
        """
        Attend son tour avant d'autoriser une requête.
        """
        async with self._lock:
            now = time.monotonic()
            delay = self._next_allowed - now
            if delay > 0:
                await asyncio.sleep(delay)
                now = time.monotonic()
            self._next_allowed = now + self.min_interval
