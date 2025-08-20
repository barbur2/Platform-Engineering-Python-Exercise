import boto3
import click
from utils import get_username
import uuid

route53 = boto3.client("route53")
username = get_username()


@click.group()
def route53_cli():
    """Manage Route53 hosted zones"""
    pass


@route53_cli.command("create")
@click.argument("domain_name")
def create_zone(domain_name):
    """Create a new Route53 hosted zone"""
    try:
        response = route53.create_hosted_zone(
            Name=domain_name,
            CallerReference=str(uuid.uuid4())
        )

        zone_id = response["HostedZone"]["Id"].split("/")[-1]

        route53.change_tags_for_resource(
            ResourceType="hostedzone",
            ResourceId=zone_id,
            AddTags=[
                {"Key": "Owner", "Value": username},
                {"Key": "CreatedBy", "Value": "platform-cli"},
            ]
        )

        click.echo(f"✅ Created hosted zone {domain_name} (id={zone_id}, owner={username})")

    except Exception as e:
        click.echo(f"❌ Error creating hosted zone {domain_name}: {e}")



@route53_cli.command("list-all")
def list_all_zones():
    """List ALL Route53 hosted zones"""
    try:
        response = route53.list_hosted_zones()
        zones = response.get("HostedZones", [])

        if not zones:
            click.echo("ℹ️ No hosted zones found.")
            return

        for zone in zones:
            zone_id = zone["Id"]
            zone_name = zone["Name"]
            tags = route53.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id.split("/")[-1])
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags.get("ResourceTagSet", {}).get("Tags", [])}
            owner = tag_dict.get("Owner", "unknown")

            click.echo(f"✅ {zone_name} (id={zone_id}, owner={owner})")

    except Exception as e:
        click.echo(f"❌ Error listing zones: {e}")


@route53_cli.command("list-mine")
def list_my_zones():
    """List ONLY Route53 hosted zones created by the current user"""
    try:
        response = route53.list_hosted_zones()
        zones = response.get("HostedZones", [])

        my_zones = []
        for zone in zones:
            zone_id = zone["Id"]
            zone_name = zone["Name"]
            tags = route53.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id.split("/")[-1])
            tag_dict = {tag["Key"]: tag["Value"] for tag in tags.get("ResourceTagSet", {}).get("Tags", [])}
            owner = tag_dict.get("Owner", "unknown")

            if owner == username:
                my_zones.append((zone_name, zone_id, owner))

        if not my_zones:
            click.echo("ℹ️ You have no hosted zones.")
            return

        for zone_name, zone_id, owner in my_zones:
            click.echo(f"✅ {zone_name} (id={zone_id}, owner={owner})")

    except Exception as e:
        click.echo(f"❌ Error listing your zones: {e}")


@route53_cli.command("delete")
@click.argument("zone_id")
def delete_zone(zone_id):
    """Delete a Route53 hosted zone"""
    try:
        response = route53.get_hosted_zone(Id=zone_id)
        zone_name = response["HostedZone"]["Name"]
        tags = route53.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id)
        tag_dict = {tag["Key"]: tag["Value"] for tag in tags.get("ResourceTagSet", {}).get("Tags", [])}
        owner = tag_dict.get("Owner", "unknown")

        if owner != username:
            confirm = click.prompt(
                f"⚠️ WARNING: You are NOT the owner of {zone_name} (owner={owner}).\n"
                f"Type 'agree' to proceed anyway",
                default="no"
            )
            if confirm.strip().lower() != "agree":
                click.echo("❎ Deletion cancelled.")
                return
            else:
                click.echo("⚠️ Proceeding despite ownership mismatch...")

        records = route53.list_resource_record_sets(HostedZoneId=zone_id)
        changes = []
        for record in records["ResourceRecordSets"]:
            if record["Type"] in ["NS", "SOA"]:
                continue
            changes.append({"Action": "DELETE", "ResourceRecordSet": record})

        if changes:
            route53.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={"Changes": changes}
            )

        route53.delete_hosted_zone(Id=zone_id)
        click.echo(f"🗑️ Deleted hosted zone {zone_name} (id={zone_id})")

    except Exception as e:
        click.echo(f"❌ Error deleting hosted zone {zone_id}: {e}")



@route53_cli.command("cleanup")
def cleanup_zones():
    """Delete ALL your hosted zones"""
    try:
        response = route53.list_hosted_zones()
        my_zones = []
        for zone in response["HostedZones"]:
            comment = zone.get("Config", {}).get("Comment", "")
            if f"owner={username}" in comment:
                my_zones.append(zone)

        if not my_zones:
            click.echo("ℹ️ You have no hosted zones to cleanup.")
            return

        confirm = click.prompt(
            f"⚠️ WARNING: This will delete ALL {len(my_zones)} zones: "
            f"{', '.join([z['Name'].rstrip('.') for z in my_zones])}\n"
            "Type 'delete all' to confirm",
            default="no"
        )

        if confirm.strip().lower() != "delete all":
            click.echo("❎ Cleanup cancelled.")
            return

        for zone in my_zones:
            zone_id = zone["Id"].replace("/hostedzone/", "")
            zone_name = zone["Name"].rstrip(".")

            # delete records except NS + SOA
            records = route53.list_resource_record_sets(HostedZoneId=f"/hostedzone/{zone_id}")
            for record in records["ResourceRecordSets"]:
                if record["Type"] in ["NS", "SOA"]:
                    continue
                route53.change_resource_record_sets(
                    HostedZoneId=f"/hostedzone/{zone_id}",
                    ChangeBatch={"Changes": [{"Action": "DELETE", "ResourceRecordSet": record}]}
                )

            # delete hosted zone
            route53.delete_hosted_zone(Id=f"/hostedzone/{zone_id}")
            click.echo(f"🗑️ Deleted hosted zone: {zone_name} (id={zone_id})")

        click.echo("✅ Cleanup finished.")

    except Exception as e:
        click.echo(f"❌ Error cleaning up hosted zones: {e}")
