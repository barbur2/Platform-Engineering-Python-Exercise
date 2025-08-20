def generate_tags(owner: str, project: str = "default", environment: str = "dev"):
    return [
        {"Key": "CreatedBy", "Value": "platform-cli"},
        {"Key": "Owner", "Value": owner},
        {"Key": "Project", "Value": project},
        {"Key": "Environment", "Value": environment},
    ]
import boto3

def get_username():
    """
    מחזיר את המשתמש שמחובר ל־AWS CLI (ה־IAM User או Role).
    """
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        # לדוגמה: arn:aws:iam::123456789012:user/bar
        arn = identity["Arn"]
        if ":user/" in arn:
            return arn.split("/")[-1]  # שם המשתמש
        elif ":assumed-role/" in arn:
            return arn.split("/")[-1]  # שם הרול
        else:
            return "unknown"
    except Exception:
        return "unknown"
