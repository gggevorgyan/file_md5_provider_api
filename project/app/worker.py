import os
from celery import Celery
import hashlib
import datetime
import logging
import multiprocessing

# --- Logging Setup ---
hostname = os.environ.get("HOSTNAME")
loglevel = os.environ.get('LOGLEVEL', 'INFO').upper()
logdir=os.environ.get('LOGDIR', '/var/log/')


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('worker_logger')
iohandler = logging.FileHandler(f"{logdir}/worker--{hostname}--{str(datetime.datetime.now())}.log")
iohandler.setFormatter(formatter)
logger.addHandler(iohandler)
logger.setLevel(loglevel)
lock = multiprocessing.Lock()

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://localhost:5672")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery.conf.result_extended=True


@celery.task(name="create_new_md5_task")
def create_md5_task(file_path):
    md5 = hashlib.md5(open(file_path,'rb').read()).hexdigest()
    os.remove(file_path)
    lock.acquire()
    logger.info(f"MD5 : {md5}")
    logger.debug(f"Processed file successfully removed from disk: {file_path}")
    lock.release()
    return md5


