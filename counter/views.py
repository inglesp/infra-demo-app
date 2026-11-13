import logging

from django.conf import settings
from django.http import HttpResponse

from counter.models import Visit

logger = logging.getLogger(__name__)


def index(request):
    Visit.objects.create()
    count = Visit.objects.count()
    logger.info("Recorded visit %d for host %s", count, request.get_host())
    return HttpResponse(
        "# Hello world\n"
        f"Host: {request.get_host()}\n"
        f"Visit count: {count}\n"
        f"Build: {settings.GIT_COMMIT}\n"
        f"Secret: {settings.DEMO_SECRET or 'not set'}\n"
        f"Non-secret: {settings.DEMO_NON_SECRET or 'not set'}\n",
        content_type="text/plain",
    )
