import marshmallow
from helper_schema import CamelCaseSchema, SimpleTypeSchema
from marshmallow import Schema, fields, post_load, pre_dump, validate
from modification_info_schema import ModificationInfoSchema
from plan_model import TransferOutPlan


class TransferOutPlanSchema(SimpleTypeSchema, CamelCaseSchema):
    """Schema for Base Tag as abstract class"""

    OBJ_CLS = TransferOutPlan

    accountNumber = fields.String(
        required=True,
        validate=[validate.Length(0, 600)],
        metadata={
            "description": "Value for the given key of a tag",
            "example": "400118490",
        },
    )
    clerkId = fields.String(
        required=True,
        validate=[validate.Length(0, 2)],
        metadata={
            "description": "Value for the given key of a tag",
            "example": "SY",
        },
    )
    month = fields.String(
        required=True,
        validate=[validate.Length(0, 3)],
        metadata={
            "description": "Value for the given key of a tag",
            "example": "JUN",
        },
    )
    isQESI = fields.Boolean()
    isResidual = fields.Boolean()


class DBTransferOutPlanSchema(TransferOutPlanSchema):
    OBJ_CLS = TransferOutPlan

    planId = fields.String(
        required=True,
        validate=[validate.Length(1, 13)],
        metadata={"description": "Key of a tag", "example": "brand"},
    )

    modificationInfo = fields.Nested(
        ModificationInfoSchema,
        required=True,
        metadata={"description": "modification info of a tag"},
    )


TRANSFER_OUT_PLAN_SCHEMA = TransferOutPlanSchema()
TRANSFER_OUT_PLAN_MANY_SCHEMA = TransferOutPlanSchema(many=True)
DB_TRANSFER_OUT_PLAN_SCHEMA = DBTransferOutPlanSchema()


# def test_chat_schema():
#     dict = {
#         "accountNumber": "400118470",
#         "clerkId": "SY",
#         "month": "JUN",
#         "isQESI": True,
#         "isResidual": True,
#     }
#     my_plan = TRANSFER_OUT_PLAN_SCHEMA.load(dict)
#     print(my_plan)
#     output_plan = DB_TRANSFER_OUT_PLAN_SCHEMA.dump(my_plan)
#     assert my_plan.modificationInfo
#     assert my_plan.planId
#     print(output_plan)


# test_chat_schema()
