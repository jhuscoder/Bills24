import time
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Simple module-level token cache
_token_cache = {
    'token': getattr(settings, 'EBILL_TOKEN', None),
    'expires_at': 0,
}


class ExternalBillingClient:
    """Client to communicate with the external e-billing provider.

    Behavior:
    - If `EBILL_TOKEN` is configured in settings, use it as a static bearer token.
    - Otherwise, attempt to authenticate against `EBILL_AUTH_URL` with
      `EBILL_USERNAME`/`EBILL_PASSWORD` to obtain a token.
    - Tokens are cached for `EBILL_TOKEN_REFRESH_SECONDS` seconds.
    """

    def __init__(self):
        self.base_url = getattr(settings, 'EBILL_URL', None)
        self.auth_url = getattr(settings, 'EBILL_AUTH_URL', None)
        self.username = getattr(settings, 'EBILL_USERNAME', None)
        self.password = getattr(settings, 'EBILL_PASSWORD', None)
        self.timeout = getattr(settings, 'EBILL_TIMEOUT', 30)
        self.token_refresh_seconds = getattr(settings, 'EBILL_TOKEN_REFRESH_SECONDS', 60 * 60 * 24 * 3)

    def _get_token(self):
        global _token_cache
        now = int(time.time())
        if _token_cache.get('token') and _token_cache.get('expires_at', 0) > now:
            return _token_cache['token']

        # If a static token is configured, use it indefinitely
        static = getattr(settings, 'EBILL_TOKEN', None)
        if static:
            _token_cache['token'] = static
            _token_cache['expires_at'] = now + self.token_refresh_seconds
            return static

        # Otherwise, get token from auth endpoint
        if not (self.auth_url and self.username and self.password):
            raise RuntimeError('No EBILL_TOKEN and no auth credentials configured')

        try:
            resp = requests.post(self.auth_url, json={'username': self.username, 'password': self.password}, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            token = data.get('token') or data.get('access') or data.get('access_token')
            if not token:
                raise RuntimeError('Auth response did not contain a token')
            _token_cache['token'] = token
            _token_cache['expires_at'] = now + self.token_refresh_seconds
            return token
        except Exception as exc:
            logger.exception('Failed to obtain authentication token from external provider: %s', exc)
            raise

    def _headers(self):
        token = self._get_token()
        return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    def post(self, path, payload):
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        print(url)
        headers = self._headers()
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError:
            try:
                return resp.json()
            except Exception:
                raise
        except Exception:
            logger.exception('Error calling external billing provider')
            raise

    def get(self, path, params=None):
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        headers = self._headers()
        try:
            resp = requests.get(url, params=params or {}, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError:
            try:
                return resp.json()
            except Exception:
                raise
        except Exception:
            logger.exception('Error calling external billing provider (GET)')
            raise

    def pay(self, service_slug, amount, account_ref, metadata=None):
        payload = {
            'service': service_slug,
            'amount': str(amount),
            'account': account_ref,
            'metadata': metadata or {},
        }
        return self.post('/payments', payload)
