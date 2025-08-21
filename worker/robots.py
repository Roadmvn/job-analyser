from urllib.parse import urlparse
import urllib.robotparser as robotparser
from functools import lru_cache


@lru_cache(maxsize=128)
def _get_robotparser(base_url: str):
    rp = robotparser.RobotFileParser()
    rp.set_url(base_url.rstrip('/') + '/robots.txt')
    try:
        rp.read()
    except Exception:
        pass
    return rp


def is_allowed(url: str, user_agent: str) -> bool:
    try:
        parts = urlparse(url)
        base = f"{parts.scheme}://{parts.netloc}"
        rp = _get_robotparser(base)
        if not rp:
            return False
        path = parts.path or '/'
        return rp.can_fetch(user_agent, path)
    except Exception:
        return False


