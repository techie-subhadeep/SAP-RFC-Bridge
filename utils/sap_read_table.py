from typing import List
from pyrfc import Connection
import os


def sap_read_table(
    sap_table: str,
    fields: List[str],
    where: List[str],
    max_rows: int,
    from_row: int,
    delimiter: str = "|",
):
    """A function to query SAP with RFC_READ_TABLE"""

    # By default, if you send a blank value for fields, you get all of them
    # Therefore, we add a select all option, to better mimic SQL.

    if fields[0] == "*":
        fields = ""
    else:
        fields = [{"FIELDNAME": x} for x in fields]  # Notice the format

    # the WHERE part of the query is called "options"
    # options = [{'TEXT': x} for x in where]  # again, notice the format

    # we set a maximum number of rows to return, because it's easy to do and
    # greatly speeds up testing queries.
    rowcount = max_rows

    # Here is the call to SAP's RFC_READ_TABLE
    connection_params = {
        "ashost": os.environ.get("SAP_AHOST"),
        "sysnr": os.environ.get("SAP_SYSNR"),
        "client": os.environ.get("SAP_CLIENT"),
        "user": os.environ.get("SAP_USER"),
        "passwd": os.environ.get("SAP_PASSWD"),
    }

    with Connection(**connection_params) as conn:
        tables = conn.call(
            "RFC_READ_TABLE",
            QUERY_TABLE=sap_table,
            DELIMITER=delimiter,
            FIELDS=fields,
            OPTIONS=[{"TEXT": x} for x in where],
            ROWCOUNT=max_rows,
            ROWSKIPS=from_row,
        )

    # We split out fields and fields_name to hold the data and the column names
    fields = []
    fields_name = []

    data_fields = tables["DATA"]  # pull the data part of the result set
    data_names = tables["FIELDS"]  # pull the field name part of the result set

    headers = [x["FIELDNAME"] for x in data_names]  # headers extraction
    long_fields = len(data_fields)  # data extraction
    long_names = len(data_names)  # full headers extraction if you want it

    # now parse the data fields into a list
    for line in range(0, long_fields):
        fields.append(data_fields[line]["WA"].strip())

    # for each line, split the list by the '|' separator
    fields = [x.strip().split(delimiter) for x in fields]

    # return the 2D list and the headers
    result = []
    for line in fields:
        data = {}
        for idx in range(len(headers)):
            k = str(headers[idx]).strip()
            v = str(line[idx]).strip()
            data[k] = v
        result.append(data)
    return result
