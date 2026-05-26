import json
import logging
from django.http import JsonResponse
from api.response import error_response
from rest_framework.renderers import JSONRenderer
from django.utils.deprecation import MiddlewareMixin
from .utils import handle_outgoing_response, handle_incoming_request

logger = logging.getLogger(__name__)

class ResponseHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Remove server-identifying header (if present) and add app headers.
        try:
            if response.has_header('Server'):
                del response['Server']
        except Exception:
            # Some response types may not implement has_header reliably
            response.headers.pop('Server', None)

        # Consider moving these values into settings later.
        response['X-App-Version'] = '1.2.0'
        response['X-Device-Id'] = 'android'
        response['X-User-Theme'] = 'dark'
        return response


class DataEncryptionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """Decrypt incoming JSON envelope payloads into the original JSON body.

        Expects incoming requests to be application/json with a body of the
        form: {"data": "<encrypted-payload>"}. Decrypts and replaces
        request._body with the decrypted JSON bytes so downstream code sees
        the original JSON object.
        """
        content_type = request.META.get('CONTENT_TYPE', '')
        if request.method in ("POST", "PUT", "PATCH") and 'application/json' in content_type:
            try:
                if not request.body:
                    return None

                # Use the full envelope string to let utils.handle_incoming_request
                # parse and decrypt correctly.
                body_text = request.body.decode(getattr(request, 'encoding', 'utf-8') or 'utf-8')
                decrypted_obj = handle_incoming_request(body_text)

                if decrypted_obj is None:
                    return error_response('Malformed or unreadable encrypted data', status_code=400)

                # Replace the request body with the decrypted JSON string
                decrypted_bytes = json.dumps(decrypted_obj).encode('utf-8')
                request._body = decrypted_bytes
                request.META['CONTENT_LENGTH'] = str(len(decrypted_bytes))
            except Exception as exc:
                logger.exception("Failed to decrypt incoming request: %s", exc)
                return error_response('Malformed or unreadable encrypted data', status_code=400)
        return None

class EncryptedJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        rendered_json = super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get('response') if renderer_context else None

        if response and response.status_code >= 400:
            return rendered_json

        # Avoid encrypting schema or docs responses (drf-spectacular)
        view = renderer_context.get('view') if renderer_context else None
        try:
            if view is not None:
                module = getattr(view.__class__, '__module__', '')
                name = getattr(view.__class__, '__name__', '')
                if module.startswith('drf_spectacular') or name in ('SpectacularAPIView', 'SpectacularSwaggerView'):
                    return rendered_json
        except Exception:
            pass

        # If the data is an OpenAPI/Swagger dict, return raw
        if isinstance(data, dict) and ('openapi' in data or 'swagger' in data):
            return rendered_json

        try:
            # `data` is already the Python object that would be rendered; use it
            # rather than re-parsing strings to avoid double-encoding.
            encrypted_envelope = handle_outgoing_response(data)
            if encrypted_envelope is None:
                return rendered_json

            return encrypted_envelope.encode('utf-8')
        except Exception:
            logger.exception('EncryptedJSONRenderer failed to encrypt response')
            return rendered_json