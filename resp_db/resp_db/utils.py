import json
import logging
from datetime import datetime

from customer_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_date_time():
    date_time = datetime.now()
    time_id = date_time.strftime("%m%d%H%M")
    return time_id


def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    if body is not None:
        logger.info(json.dumps(body, cls=CustomEncoder))
        response["body"] = json.dumps(body, cls=CustomEncoder)
    return response
