import boto3
import click
from utils import get_username

session = boto3.session.Session()
ec2 = session.client("ec2")
username = get_username()


@click.group()
def ec2_cli():
    """Manage EC2 instances"""
    pass


@ec2_cli.command("list")
def list_instances():
    """List EC2 instances"""
    try:
        response = ec2.describe_instances()
        reservations = response.get("Reservations", [])
        if not reservations:
            click.echo("ℹ️ No instances found.")
            return

        for reservation in reservations:
            for instance in reservation["Instances"]:
                state = instance["State"]["Name"]
                iid = instance["InstanceId"]
                click.echo(f"💻 {iid} [{state}]")
    except Exception as e:
        click.echo(f"❌ Error listing instances: {e}")


@ec2_cli.command("terminate-all")
def terminate_all_instances():
    """Terminate ALL your instances"""
    try:
        response = ec2.describe_instances(
            Filters=[
                {"Name": "tag:CreatedBy", "Values": ["platform-cli"]},
                {"Name": "tag:Owner", "Values": [username]},
            ]
        )
        instance_ids = []
        for r in response["Reservations"]:
            for inst in r["Instances"]:
                if inst["State"]["Name"] not in ["terminated", "shutting-down"]:
                    instance_ids.append(inst["InstanceId"])

        if not instance_ids:
            click.echo("ℹ️ No instances to terminate.")
            return

        confirm = click.prompt(
            f"⚠️ WARNING: This will delete ALL {len(instance_ids)} instances: {', '.join(instance_ids)}\n"
            "Type 'delete all' to confirm",
            default=""
        )
        if confirm.strip().lower() != "delete all":
            click.echo("❎ Termination cancelled.")
            return

        ec2.terminate_instances(InstanceIds=instance_ids)
        click.echo(f"💀 Terminated instances: {', '.join(instance_ids)}")

    except Exception as e:
        click.echo(f"❌ Error terminating: {e}")

