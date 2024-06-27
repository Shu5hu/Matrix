import csv
import json
import subprocess

# Define the AWS region
region = 'us-east-1'

# Function to run AWS CLI commands
def run_aws_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# List EC2 instances
ec2_instances = run_aws_command(['aws', 'ec2', 'describe-instances', '--region', region])
ec2_resources = [
    {
        'ResourceType': 'EC2 Instance',
        'ResourceId': instance['InstanceId'],
        'ResourceName': next(
            (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A'
        )
    }
    for reservation in ec2_instances['Reservations']
    for instance in reservation['Instances']
]

# List S3 buckets
s3_buckets = run_aws_command(['aws', 's3api', 'list-buckets'])
s3_resources = [
    {
        'ResourceType': 'S3 Bucket',
        'ResourceId': bucket['Name'],
        'ResourceName': bucket['Name']
    }
for bucket in s3_buckets['Buckets']
]

# List RDS instances
rds_instances = run_aws_command(['aws', 'rds', 'describe-db-instances', '--region', region])
rds_resources = [
    {
        'ResourceType': 'RDS Instance',
        'ResourceId': db_instance['DBInstanceIdentifier'],
        'ResourceName': db_instance['DBInstanceIdentifier']
    }
    for db_instance in rds_instances['DBInstances']
]

# Combine all resources
all_resources = ec2_resources + s3_resources + rds_resources

# Define the CSV file path
csv_file = 'aws_resources_with_names.csv'

# Define the CSV headers
headers = ['ResourceType', 'ResourceId', 'ResourceName']

# Write the resources to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for resource in all_resources:
        writer.writerow(resource)

print(f"Resources have been written to {csv_file}")
                            
