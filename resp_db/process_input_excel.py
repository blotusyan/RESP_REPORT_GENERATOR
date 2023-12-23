import json
import os
from datetime import datetime

from openpyxl import load_workbook

source_dir = os.path.dirname(__file__)
os.chdir(source_dir)
hash_map = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUN",
    7: "JUL",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC",
}
for dirpath, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
        if "xlsx" in filename:
            data_file = filename

            # Load the entire workbook.
            wb = load_workbook(data_file)

            # Load one worksheet.
            ws = wb["Sheet1"]
            all_rows = list(ws.rows)
            list_plan = []
            for row in all_rows:
                if isinstance(row[0].value, int):
                    list_plan.append(
                        {
                            "accountNumber": str(row[0].value),
                            "clerkId": row[1].value,
                            "month": hash_map[datetime.now().month],
                            "isQESI": bool(row[2].value),
                            "isResidual": bool(row[3].value),
                        }
                    )
            print(list_plan)
