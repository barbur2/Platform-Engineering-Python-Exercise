import boto3
import click
from utils import get_username

session = boto3.session.Session()
s3 = session.client("s3")
username = get_username()

import botocore


@click.group()
def s3_cli():
    """Manage S3 buckets and objects"""
    pass


@s3_cli.command("list-all")
def list_all_buckets():
    """List ALL buckets"""
    try:
        response = s3.list_buckets()
        buckets = response.get("Buckets", [])
        if not buckets:
            click.echo("ℹ️ No buckets found.")
            return

        for bucket in buckets:
            name = bucket["Name"]
            click.echo(f"🪣 {name}")
    except Exception as e:
        click.echo(f"❌ Error listing buckets: {e}")


@s3_cli.command("list-mine")
def list_my_buckets():
    """List ONLY buckets owned by you"""
    try:
        response = s3.list_buckets()
        buckets = response.get("Buckets", [])
        my_buckets = [b for b in buckets if username in b["Name"]]

        if not my_buckets:
            click.echo("ℹ️ No buckets found for you.")
            return

        for bucket in my_buckets:
            click.echo(f"🪣 {bucket['Name']} (owner={username})")
    except Exception as e:
        click.echo(f"❌ Error listing your buckets: {e}")


@s3_cli.command("create")
@click.argument("bucket_name")
def create_bucket(bucket_name):
    """Create a bucket"""
    try:
        region = session.region_name or "us-east-1"
        click.echo(f"🌍 Using region: {region}")

        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )

        click.echo(f"🪣 Created bucket: {bucket_name} (owner={username})")
    except Exception as e:
        click.echo(f"❌ Error creating bucket {bucket_name}: {e}")


@s3_cli.command("delete")
@click.argument("bucket_name")
def delete_bucket(bucket_name):
    """Delete a bucket"""
    try:
        # נבדוק אם זה שלך
        if username not in bucket_name:
            confirm = click.prompt(
                f"⚠️ WARNING: You are NOT the owner of {bucket_name}.\n"
                "Type EXACTLY 'agree' to proceed anyway",
                default=""
            )

            if confirm.strip().lower() != "agree":
                click.echo("❎ Deletion cancelled.")
                return

        # קודם ננקה אובייקטים
        objects = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
        for obj in objects:
            key = obj["Key"]
            s3.delete_object(Bucket=bucket_name, Key=key)
            click.echo(f"🗑️ Deleted {key} from {bucket_name}")

        s3.delete_bucket(Bucket=bucket_name)
        click.echo(f"🪣 Deleted bucket: {bucket_name}")

    except Exception as e:
        click.echo(f"❌ Error deleting bucket {bucket_name}: {e}")
