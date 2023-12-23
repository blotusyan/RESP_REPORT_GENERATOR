import logging

import boto3
from boto3.dynamodb.conditions import Attr, Key
from config import DYNAMODB_TABLE
from plan_schema import DB_TRANSFER_OUT_PLAN_SCHEMA, TRANSFER_OUT_PLAN_SCHEMA
from utils import buildResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamoDB = DYNAMODB_TABLE
client = boto3.resource("dynamodb")
table = client.Table(dynamoDB)


def save_db(my_TransferOutPlans):
    output_list = []
    for my_TransferOutPlan in my_TransferOutPlans:
        my_pk = my_TransferOutPlan.month
        my_sk_1 = "#".join(
            [my_TransferOutPlan.clerkId, my_TransferOutPlan.accountNumber]
        )
        db_serialized_chat = DB_TRANSFER_OUT_PLAN_SCHEMA.dump(my_TransferOutPlan)
        output_serialized_chat = TRANSFER_OUT_PLAN_SCHEMA.dump(my_TransferOutPlan)
        item = {
            "pk": my_pk,
            "sk-1": my_sk_1,
            "data": db_serialized_chat,
        }
        table.put_item(Item=item)
        output_list.append(output_serialized_chat)
    body = {"Operation": "Save", "Message": "Success", "Items": output_list}
    return buildResponse(200, body)


def get_month_db(month, is_QESI, is_residual):
    hash_key = Key("pk")
    range_key = Key("sk-1")

    key_condition_expression = hash_key.eq(month)
    kwargs = {"KeyConditionExpression": key_condition_expression}

    response = table.query(**kwargs)
    if response["Items"]:
        logger.info(response["Items"])
        output_list = []
        for item in response["Items"]:
            my_flag = False
            logger.info(my_flag)
            deserial_db = DB_TRANSFER_OUT_PLAN_SCHEMA.load(item["data"])
            serial_output = TRANSFER_OUT_PLAN_SCHEMA.dump(deserial_db)
            logger.info("is_QESI and is_residual are: ")
            logger.info(
                {
                    "QESI": is_QESI,
                    "RESIDUAL": is_residual,
                    "check QESI": is_QESI is True,
                    "check residual": bool(serial_output["isQESI"]) is True,
                    "check residual without bool": serial_output["isQESI"] is True,
                }
            )
            if is_QESI == "True" and serial_output["isQESI"] is True:
                my_flag = True
                logger.info("yes qesi will be provided")
            else:
                logger.info("no qesi will not be provided")
            if is_residual == "True" and serial_output["isResidual"] is True:
                my_flag = True
                logger.info("yes residual will be provided")
            else:
                logger.info("no residual will not be provided")
            if my_flag is True:
                logger.info("yes thats it")
                output_list.append(serial_output)
            else:
                logger.info("wont be displayed")
        summary_list = []
        summary_list.append("##SUMMARY OF RESP TRANSFER PROCESSED IN: " + month + "##")
        count = 1
        for each_output in output_list:
            each_line = (
                "["
                + str(count)
                + "]"
                + "--"
                + each_output["accountNumber"]
                + "--Clerk:"
                + each_output["clerkId"]
                + "--"
                + ("with QESI" if each_output["isQESI"] is True else "without QESI")
                + "--"
                + (
                    "with residual"
                    if each_output["isResidual"] is True
                    else "without residual"
                )
            )
            count += 1
            summary_list.append(each_line)
        return buildResponse(200, summary_list)
    else:
        return buildResponse(404, {"Message": "%s RESP not found" % month})


def query_clerk_db(clerkId, month, is_QESI, is_residual):
    response = table.scan()
    # Check if the scan operation was successful
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        # Print out each item in the table
        if response["Items"]:
            clerk_list = []
            for item in response["Items"]:
                deserial_db = DB_TRANSFER_OUT_PLAN_SCHEMA.load(item["data"])
                serial_output = TRANSFER_OUT_PLAN_SCHEMA.dump(deserial_db)
                if serial_output["clerkId"] == clerkId:
                    clerk_list.append(serial_output)
            output_clerk_list = []
            if month == "False":
                output_clerk_list = clerk_list
            else:
                for clerk_item in clerk_list:
                    my_flag = False
                    if clerk_item["month"] == month:
                        if is_QESI == "True" and clerk_item["isQESI"] is True:
                            my_flag = True
                            logger.info("yes qesi will be provided")
                        else:
                            logger.info("no qesi will not be provided")
                        if is_residual == "True" and clerk_item["isResidual"] is True:
                            my_flag = True
                            logger.info("yes residual will be provided")
                        else:
                            logger.info("no residual will not be provided")
                        if my_flag is True:
                            logger.info("yes thats it")
                            output_clerk_list.append(clerk_item)
                        else:
                            logger.info("wont be displayed")

            summary_list = []
            summary_list.append(
                "##SUMMARY OF RESP TRANSFER PROCESSED BY: " + clerkId + "##"
            )
            count = 1
            for each_output in output_clerk_list:
                each_line = (
                    "["
                    + str(count)
                    + "]"
                    + "--"
                    + each_output["accountNumber"]
                    + "--Clerk:"
                    + each_output["clerkId"]
                    + "--"
                    + ("with QESI" if each_output["isQESI"] is True else "without QESI")
                    + "--"
                    + (
                        "with residual"
                        if each_output["isResidual"] is True
                        else "without residual"
                    )
                )
                count += 1
                summary_list.append(each_line)
            return buildResponse(200, summary_list)
        else:
            return buildResponse(404, {"Message": "id: %s not found" % clerkId})


def query_all():
    response = table.scan()
    # Check if the scan operation was successful
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        # Print out each item in the table
        if response["Items"]:
            output_list = []
            for item in response["Items"]:
                deserial_db = DB_TRANSFER_OUT_PLAN_SCHEMA.load(item["data"])
                serial_output = TRANSFER_OUT_PLAN_SCHEMA.dump(deserial_db)
                output_list.append(serial_output)
            summary_list = []
            summary_list.append("##SUMMARY OF ALL RESP TRANSFER IN DATABASE##")
            count = 1
            for each_output in output_list:
                each_line = (
                    "["
                    + str(count)
                    + "]"
                    + "--"
                    + each_output["accountNumber"]
                    + "--Clerk:"
                    + each_output["clerkId"]
                    + "--"
                    + ("with QESI" if each_output["isQESI"] is True else "without QESI")
                    + "--"
                    + (
                        "with residual"
                        if each_output["isResidual"] is True
                        else "without residual"
                    )
                )
                count += 1
                summary_list.append(each_line)
            return buildResponse(200, summary_list)
        else:
            return buildResponse(404, {"Message": "No item found"})
