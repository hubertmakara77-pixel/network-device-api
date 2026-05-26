from pysnmp.hlapi import *

def fetch_snmp_metric(ip_address, community, oid, port=161):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1),
        UdpTransportTarget((ip_address, port), timeout=2.0, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        return {"error": str(errorIndication)}
    elif errorStatus:
        return {"error": f"{errorStatus.prettyPrint()} at {errorIndex}"}
    else:
        for varBind in varBinds:
            return {"value": str(varBind[1])}