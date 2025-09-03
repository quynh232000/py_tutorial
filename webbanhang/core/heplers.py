import pprint, sys, logging, random, string
from datetime import datetime
from django.http import JsonResponse
def dump(*args):
    for arg in args:
        pprint.pprint(arg)

def dd(*args):
    dump(*args)
    sys.exit()

def log_debug(message):
    logger = logging.getLogger(__name__)
    logger.debug(message)
    print(f"[DEBUG] {message}")

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
def dd_browser(data):
    """Dump ra browser dưới dạng JSON rồi dừng"""
    return JsonResponse(data, safe=False)