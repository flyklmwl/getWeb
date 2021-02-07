import logging
import traceback
import os

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
curtpath = os.path.abspath(os.path.dirname(__file__))
handler = logging.FileHandler(curtpath + "/../../logs/log.txt")
# handler = logging.FileHandler("../logs/log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(pathname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)
# logger.exception(sys.exc_info())


def logtrace(actual_do):
    def add_logtrace(*args, **kwargs):
        try:
            return actual_do(*args, **kwargs)
        except:
            s = traceback.format_exc()
            logger.error(s)
    return add_logtrace
