import csv
import json
import subprocess
import argparse

# Function to run AWS CLI commands
def run_aws_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Function to list AWS resources
def list_resources(region):
    # List EC2 instances
    ec2_instances = run_aws_command(['aws', 'ec2', 'describe-instances', '--region', region])
    ec2_resources = [
        {
            'ResourceType': 'EC2 Instance',
            'ResourceId': instance['InstanceId'],
            'ResourceName': next(
                (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A'
            ),
            'Region': region
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
            'ResourceName': bucket['Name'],
            'Region': region
        }
        for bucket in s3_buckets['Buckets']
    ]

    # List RDS instances
    rds_instances = run_aws_command(['aws', 'rds', 'describe-db-instances', '--region', region])
    rds_resources = [
        {
            'ResourceType': 'RDS Instance',
            'ResourceId': db_instance['DBInstanceIdentifier'],
            'ResourceName': db_instance['DBInstanceIdentifier'],
            'Region': region
        }
        for db_instance in rds_instances['DBInstances']
    ]

    # List Elastic Beanstalk environments
    esb_environments = run_aws_command(['aws', 'elasticbeanstalk', 'describe-environments', '--region', region])
    esb_resources = [
        {
            'ResourceType': 'Elastic Beanstalk Environment',
            'ResourceId': env['EnvironmentId'],
            'ResourceName': env['EnvironmentName'],
            'Region': region
        }
        for env in esb_environments['Environments']
    ]

    # List Elastic Load Balancers
    elbs = run_aws_command(['aws', 'elb', 'describe-load-balancers', '--region', region])
    elb_resources = [
        {
            'ResourceType': 'Elastic Load Balancer',
            'ResourceId': elb['LoadBalancerName'],
            'ResourceName': elb['LoadBalancerName'],
            'Region': region
        }
        for elb in elbs['LoadBalancerDescriptions']
    ]

    # List NAT Gateways
    nat_gateways = run_aws_command(['aws', 'ec2', 'describe-nat-gateways', '--region', region])
    nat_resources = [
        {
            'ResourceType': 'NAT Gateway',
            'ResourceId': nat['NatGatewayId'],
            'ResourceName': 'N/A',  # NAT Gateways do not have names by default
            'Region': region
        }
        for nat in nat_gateways['NatGateways']
    ]

    # List Elastic IPs
    elastic_ips = run_aws_command(['aws', 'ec2', 'describe-addresses', '--region', region])
    elastic_ip_resources = [
        {
            'ResourceType': 'Elastic IP',
            'ResourceId': address['PublicIp'],
            'ResourceName': next(
                (tag['Value'] for tag in address.get('Tags', []) if tag['Key'] == 'Name'), 'N/A'
            ),
            'Region': region
        }
        for address in elastic_ips['Addresses']
    ]

    # Combine all resources
    return ec2_resources + s3_resources + rds_resources + esb_resources + elb_resources + nat_resources + elastic_ip_resources

# Main function
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='List AWS resources and write them to a CSV file.')
    parser.add_argument('--region', type=str, required=True, help='The AWS region to list resources from')
    args = parser.parse_args()

    # Get resources from the specified region
    resources = list_resources(args.region)

    # Define the CSV file path
    csv_file = f'aws_resources_{args.region}.csv'

    # Define the CSV headers
    headers = ['ResourceType', 'ResourceId', 'ResourceName', 'Region']

    # Write the resources to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for resource in resources:
            writer.writerow(resource)

    print(f"Resources have been written to {csv_file}")

if __name__ == '__main__':
    main()
