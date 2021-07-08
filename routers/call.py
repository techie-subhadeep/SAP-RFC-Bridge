from typing import Any, Dict, List
from utils.sap_call import sap_call, sap_ping
from utils.sap_read_table import sap_read_table
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from fastapi.responses import Response


router = APIRouter()


class RFCResponse(BaseModel):
    status: str
    message: str
    data: Any


@router.get(
    "/ping",
    description="""
    Check Connectivity
    """,
)
async def ping(response: Response):
    try:
        return sap_ping()
    except Exception as e:
        response.status_code = 500
        response.media_type = "text/plain"
        return str(e)


@router.post(
    "/call/{rfc_name}",
    description="""
    Call SAP ECC RFC 
    """,
    response_model=RFCResponse,
    response_class=ORJSONResponse,
)
async def kite_call(rfc_name: str, parameters: Dict[str, Any]):
    status = "success"
    message = ""
    data = {}

    try:
        data = sap_call(rfc_name, **parameters)
        status = "success"
    except Exception as e:
        status = "error"
        message = str(e)
    finally:
        return RFCResponse(status=status, message=message, data=data)


class ReadTableRequest(BaseModel):
    fields: List[str]
    where: List[str]
    max_rows: int = 100
    skip_rows: int = 0


@router.post(
    "/read-table/{table_name}",
    description="""
    Read data from table (internaly uses RFC_READ_TABLE) 
    """,
    response_model=RFCResponse,
    response_class=ORJSONResponse,
)
async def read_table(table_name: str, params: ReadTableRequest):
    status = "success"
    message = ""
    data = {}

    try:
        data = sap_read_table(
            sap_table=table_name,
            fields=params.fields,
            where=params.where,
            max_rows=params.max_rows,
            from_row=params.skip_rows,
            delimiter="|",
        )
        status = "success"
    except Exception as e:
        status = "error"
        message = str(e)
    finally:
        return RFCResponse(status=status, message=message, data=data)