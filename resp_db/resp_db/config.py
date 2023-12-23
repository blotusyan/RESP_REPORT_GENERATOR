import os
from os import getenv

DYNAMODB_TABLE = getenv(
    "DYNAMODB_TABLE", "resp-db-DynamoDB-1V1J2BMT75NQ-RESPTable-11P13BD92I1J2"
)
