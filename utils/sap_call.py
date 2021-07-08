from pyrfc import Connection
import os


def sap_ping():
    connection_params = {
        "ashost": os.environ.get("SAP_AHOST"),
        "sysnr": os.environ.get("SAP_SYSNR"),
        "client": os.environ.get("SAP_CLIENT"),
        "user": os.environ.get("SAP_USER"),
        "passwd": os.environ.get("SAP_PASSWD"),
    }
    with Connection(**connection_params) as conn:
        return conn.get_connection_attributes()


def sap_call(rfc_name, **kwargs):
    connection_params = {
        "ashost": os.environ.get("SAP_AHOST"),
        "sysnr": os.environ.get("SAP_SYSNR"),
        "client": os.environ.get("SAP_CLIENT"),
        "user": os.environ.get("SAP_USER"),
        "passwd": os.environ.get("SAP_PASSWD"),
    }

    with Connection(**connection_params) as conn:
        return conn.call(rfc_name, **kwargs)
