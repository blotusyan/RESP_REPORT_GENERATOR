import json
import logging
from dataclasses import dataclass
from datetime import datetime

from modification_info_model import ModificationInfo
from utils import create_date_time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class TransferOutPlan:
    """Properties for TransferOutPlan"""

    accountNumber: str
    clerkId: str
    month: str
    isQESI: bool
    isResidual: bool
    modificationInfo: ModificationInfo
    planId: str

    def __init__(self, **kwargs):
        self.accountNumber = kwargs.get("accountNumber")
        self.clerkId = kwargs.get("clerkId")
        self.month = kwargs.get("month")
        self.isQESI = kwargs.get("isQESI")
        self.isResidual = kwargs.get("isResidual")
        self.planId = self.accountNumber + "-" + self.clerkId
        self.modificationInfo = ModificationInfo(
            created=datetime.now(),
            last_modified=datetime.now(),
            created_by=self.clerkId,
            last_modified_by=self.clerkId,
        )


# def test():
#     my_plan = TransferOutPlan(accountNumber="400118470", clerkId="SY", month="JUN", isQESI=True, isResidual=True)
#     print(my_plan)

# test()
