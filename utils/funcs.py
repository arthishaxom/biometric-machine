import resend
import resend.exceptions
import config
from datetime import datetime
def sendOtp(emailAddress: str, otp: str):
    resend.api_key = config.RESEND_KEY

    params: resend.Emails.SendParams = {
        "from": "KIIT HIVE <kiithive@ashishpothal.tech>",
        "to": [emailAddress],
        "subject": "OTP for Verification",
        "html": f"Your OTP is <strong>{otp}</strong>. It is valid for only 5 minutes only",
    }
    try:
        email = resend.Emails.send(params)
    except resend.exceptions.ResendError as e:
        print(f"Error - {e}")
        return "error"

def getInfo(email:str):
    yearDiff = (datetime.now().year % 100) - int(email.split("@")[0][0:2])
    month = datetime.now().month
    if(month<6):
        year=yearDiff
    else:
        year=yearDiff+1
    return year