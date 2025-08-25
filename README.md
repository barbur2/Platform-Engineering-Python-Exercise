# Platform Engineering Python Exercise
🎯 What this tool does
This is a Python CLI tool that provisions and manages AWS resources (EC2, S3, Route53) in a 
controlled and secure way.

All resources created by the CLI are tagged consistently with:
CreatedBy=platform-cli
Owner=<username>
Project=<project>
Student=bar (used to separate your resources from the rest of the class)

This ensures that the CLI never touches resources created outside of this tool.

## 📦 Prerequisites
Python 3.9+
AWS account with permissions for EC2, S3, Route53

AWS profile configured locally (aws configure) or an IAM role available

Install dependencies:
pip install -r requirements.txt
requirements.txt contains:
boto3
click

## 🚀 Running the CLI
To see all available commands:
python cli.py --help

Each resource group has its own set of commands:
python cli.py ec2 --help
python cli.py s3 --help
python cli.py route53 --help
python cli.py cleanup --help

## 💻 EC2 Usage Examples
Create an instance
python cli.py ec2 create --type t3.micro --project demo

List CLI-created instances
python cli.py ec2 list

Stop an instance
python cli.py ec2 stop --id i-xxxxxxxx

Start an instance
python cli.py ec2 start --id i-xxxxxxxx

## 🪣 S3 Usage Examples
Create a private bucket
python cli.py s3 create --name bar-bucket-test-1 --visibility private --project demo

Create a public bucket (requires confirmation)
python cli.py s3 create --name bar-bucket-test-2 --visibility public --project demo

List CLI-created buckets
python cli.py s3 list

Upload a file
echo "hello world" > test.txt
python cli.py s3 upload --name bar-bucket-test-1 --file test.txt

## 🌐 Route53 Usage Examples
Create a hosted zone
python cli.py route53 create-zone --name bar-test-domain.com --project demo

List CLI-created zones
python cli.py route53 list-zones

Create a DNS record
python cli.py route53 create-record \
  --zone-id /hostedzone/Z059923621I6CZ01H35IJ \
  --name www.bar-test-domain.com \
  --type A \
  --value 1.2.3.4

Update the record
python cli.py route53 update-record \
  --zone-id /hostedzone/Z059923621I6CZ01H35IJ \
  --name www.bar-test-domain.com \
  --type A \
  --value 5.6.7.8

Delete the record
python cli.py route53 delete-record \
  --zone-id /hostedzone/Z059923621I6CZ01H35IJ \
  --name www.bar-test-domain.com \
  --type A \
  --value 5.6.7.8

## 🧹 Cleanup
Delete all resources created by your CLI (EC2 / S3 / Route53 with Student=bar tag):
python cli.py cleanup all

## ✅ Definition of Done (DoD)
CLI enforces constraints:
EC2: only t3.micro or t2.small, maximum 2 running
S3: confirmation required for public buckets, uploads only to CLI buckets
Route53: zones and records managed only if created by CLI

All resources consistently tagged
No secrets stored in the repo (AWS profiles/roles used)
Cleanup command included to delete resources
README contains usage examples and installation steps
