from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import config
from datetime import datetime


def sendOtp(emailAddress: str, otp: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = config.BREVO_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
    subject = "Verify KIIT HIVE OTP"
    html_content = (
        f"<html><body><p>Your OTP - <strong>{otp}</strong>. Valid for 5 minutes only. </p></body></html>"
    )
    sender = {"name": "KIIT HIVE", "email": "kiithive@ashishpothal.tech"}
    to = [{"email": f"{emailAddress}"}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        sender=sender,
        subject=subject,
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        # pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return "error"


def getInfo(email: str):
    yearDiff = (datetime.now().year % 100) - int(email.split("@")[0][0:2])
    month = datetime.now().month
    if month < 6:
        year = yearDiff
    else:
        year = yearDiff + 1
    return year
