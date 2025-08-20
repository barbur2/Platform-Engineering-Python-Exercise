import boto3
import click
from utils import get_username

session = boto3.session.Session()
ec2 = session.client("ec2")
s3 = session.client("s3")
username = get_username()


@click.group()
def cleanup_cli():
    """Cleanup all resources"""
    pass


@cleanup_cli.command("all")
def cleanup_all():
    """Delete ALL EC2 + S3 created by platform-cli"""
    warning = (
        "⚠️ WARNING: This will delete ALL resources created by platform-cli!\n"
        "This includes EC2 instances and S3 buckets (with all objects).\n"
        "Type 'clean all' to confirm"
    )
    confirm = click.prompt(warning, default="")
    if confirm.strip().lower() != "clean all":
        click.echo("❎ Cleanup cancelled.")
        return

    # מחיקת אינסטנסים
    try:
        response = ec2.describe_instances(
            Filters=[
                {"Name": "tag:CreatedBy", "Values": ["platform-cli"]},
                {"Name": "tag:Owner", "Values": [username]},
            ]
        )
        for r in response["Reservations"]:
            for inst in r["Instances"]:
                if inst["State"]["Name"] not in ["terminated", "shutting-down"]:
                    iid = inst["InstanceId"]
                    ec2.terminate_instances(InstanceIds=[iid])
                    click.echo(f"💀 Terminated {iid}")
    except Exception as e:
        click.echo(f"❌ Error cleaning EC2: {e}")

    # מחיקת באקטים
    try:
        buckets = s3.list_buckets().get("Buckets", [])
        for b in buckets:
            name = b["Name"]
            if username not in name:
                continue

            objects = s3.list_objects_v2(Bucket=name).get("Contents", [])
            for obj in objects:
                key = obj["Key"]
                s3.delete_object(Bucket=name, Key=key)
                click.echo(f"🗑️ Deleted {key} from {name}")

            s3.delete_bucket(Bucket=name)
            click.echo(f"🪣 Deleted bucket: {name}")

    except Exception as e:
        click.echo(f"❌ Error cleaning S3: {e}")

    click.echo("✅ Cleanup finished.")
