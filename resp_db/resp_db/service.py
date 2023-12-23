import json
import logging

import db
from customer_encoder import CustomEncoder
from plan_schema import DB_TRANSFER_OUT_PLAN_SCHEMA, TRANSFER_OUT_PLAN_SCHEMA

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def saveProduct(my_TransferOutPlan):
    try:
        return db.save_db(my_TransferOutPlan)
    except:
        logger.exception("Do cutom exception")


def getProductbyMonth(month, is_QESI=None, is_residual=None):
    try:
        return db.get_month_db(month, is_QESI, is_residual)
    except:
        logger.exception("Do cutom exception")


def getProductbyClerk(clerk, month, is_QESI, is_residual):
    try:
        return db.query_clerk_db(clerk, month, is_QESI, is_residual)
    except:
        logger.exception("Do cutom exception")


def getAll():
    try:
        return db.query_all()
    except:
        logger.exception("Do cutom exception")
