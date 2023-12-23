import json
import logging

import service
from plan_model import TransferOutPlan
from plan_schema import TRANSFER_OUT_PLAN_MANY_SCHEMA

logger = logging.getLogger()
logger.setLevel(logging.INFO)

MONTH_PATH = "month"
CLERK_PATH = "clerkId"
RESIDUAL_PATH = "is_residual"
QESI_PATH = "is_QESI"


def register_input_handler(event, context):
    logger.info(event)
    logger.info(event["body"])
    account_list: list[dict] = process_input(event["body"])
    my_TransferOutPlans: list[TransferOutPlan] = TRANSFER_OUT_PLAN_MANY_SCHEMA.load(
        account_list
    )
    return service.saveProduct(my_TransferOutPlans)


def retrieve_by_month_handler(event, context):
    logger.info(event)
    month = event["queryStringParameters"][MONTH_PATH]
    is_QESI = event["queryStringParameters"].get(QESI_PATH, "True")
    is_residual = event["queryStringParameters"].get(RESIDUAL_PATH, "True")
    return service.getProductbyMonth(month, is_QESI, is_residual)


def retrieve_by_clerk_handler(event, context):
    logger.info(event)
    month = event["queryStringParameters"].get(MONTH_PATH, "False")
    is_QESI = event["queryStringParameters"].get(QESI_PATH, "True")
    is_residual = event["queryStringParameters"].get(RESIDUAL_PATH, "True")
    clerk = event["queryStringParameters"][CLERK_PATH]
    return service.getProductbyClerk(clerk, month, is_QESI, is_residual)


def retrieve_all(event, context):
    logger.info(event)
    return service.getAll()


def process_input(plans: str):
    logger.info("##" + plans + "##")
    deserialized_body = json.loads(plans)
    logger.info(deserialized_body)
    return deserialized_body["input"]

    # return [{
    #         "accountNumber": "400118470",
    #         "clerkId": "SY",
    #         "month": "JUN",
    #         "isQESI": True,
    #         "isResidual": True,
    #         },
    #         {
    #         "accountNumber": "400118471",
    #         "clerkId": "DT",
    #         "month": "JUN",
    #         "isQESI": True,
    #         "isResidual": True,
    #         }
    #     ]


# dict = {'resource': '/hello', 'path': '/hello', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '577', 'CloudFront-Viewer-Country': 'CA', 'Content-Type': 'application/json', 'Host': 'imroou7if7.execute-api.us-east-1.amazonaws.com', 'Postman-Token': '496567a8-b809-4ef3-aac4-056dbb307440', 'User-Agent': 'PostmanRuntime/7.31.1', 'Via': '1.1 fe2c65104051140806cad998f531e478.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'GyuJE1-DuWpDsZmtRKfmeciC1zkLnjnFL2WY2hoa2AFItRRtwk7XJQ==', 'X-Amzn-Trace-Id': 'Root=1-6413e2c2-7c9349ae69452f89110552b5', 'X-Forwarded-For': '76.68.101.130, 130.176.130.75', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['577'], 'CloudFront-Viewer-Country': ['CA'], 'Content-Type': ['application/json'], 'Host': ['imroou7if7.execute-api.us-east-1.amazonaws.com'], 'Postman-Token': ['496567a8-b809-4ef3-aac4-056dbb307440'], 'User-Agent': ['PostmanRuntime/7.31.1'], 'Via': ['1.1 fe2c65104051140806cad998f531e478.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['GyuJE1-DuWpDsZmtRKfmeciC1zkLnjnFL2WY2hoa2AFItRRtwk7XJQ=='], 'X-Amzn-Trace-Id': ['Root=1-6413e2c2-7c9349ae69452f89110552b5'], 'X-Forwarded-For': ['76.68.101.130, 130.176.130.75'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'amt2ok', 'resourcePath': '/hello', 'httpMethod': 'POST', 'extendedRequestId': 'B6BecEa1oAMFS5A=', 'requestTime': '17/Mar/2023:03:47:14 +0000', 'path': '/Prod/hello', 'accountId': '544025597035', 'protocol': 'HTTP/1.1', 'stage': 'Prod', 'domainPrefix': 'imroou7if7', 'requestTimeEpoch': 1679024834589, 'requestId': '1b7c509c-1a07-4399-8c52-946e14cfe8cb', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '76.68.101.130', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.31.1', 'user': None}, 'domainName': 'imroou7if7.execute-api.us-east-1.amazonaws.com', 'apiId': 'imroou7if7'}, 'body': '{\n    "question": "说1个张国荣成名曲"\n}', 'isBase64Encoded': False}
# print(dict["requestContext"]["accountId"])
