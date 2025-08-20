import click
from ec2_manager import ec2_cli
from s3_manager import s3_cli
from cleanup_manager import cleanup_cli
from route53_manager import route53_cli  # אם יש לך קובץ כזה


@click.group()
def cli():
    """Platform Engineering CLI"""
    pass


# מוסיפים את הקבוצות
cli.add_command(ec2_cli, name="ec2")
cli.add_command(s3_cli, name="s3")
cli.add_command(cleanup_cli, name="cleanup")
cli.add_command(route53_cli, name="route53")


if __name__ == "__main__":
    cli()
