import logging
import time
import uuid
logger = logging.getLogger('auditoria')
class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        start = time.monotonic()
        request_id = uuid.uuid4().hex
        response = self.get_response(request)
        response['X-Request-ID'] = request_id
        response['Content-Security-Policy'] = "default-src 'self'; style-src 'self'; img-src 'self'; script-src 'none'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'"
        logger.info('id=%s method=%s path=%s status=%s user_id=%s ms=%.1f',
            request_id, request.method, request.path, response.status_code,
            getattr(request.user, 'pk', None), (time.monotonic()-start)*1000)
        return response
