import argparse
import csv
import json
import subprocess

# Function to run AWS CLI commands
def run_aws_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Function to get EC2 instances
def get_ec2_instances(region):
    ec2_instances = run_aws_command(['aws', 'ec2', 'describe-instances', '--region', region])
    return [
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

# Function to get EBS volumes
def get_ebs_volumes(region):
    ebs_volumes = run_aws_command(['aws', 'ec2', 'describe-volumes', '--region', region])
    return [
        {
            'ResourceType': 'EBS Volume',
            'ResourceId': volume['VolumeId'],
            'ResourceName': next(
                (tag['Value'] for tag in volume.get('Tags', []) if tag['Key'] == 'Name'), 'N/A'
            )
        }
        for volume in ebs_volumes['Volumes']
    ]

# Function to get ELB (Classic) load balancers
def get_elb_load_balancers(region):
    elb_load_balancers = run_aws_command(['aws', 'elb', 'describe-load-balancers', '--region', region])
    return [
        {
            'ResourceType': 'Elastic Load Balancer',
            'ResourceId': elb['LoadBalancerName'],
            'ResourceName': elb['LoadBalancerName']
        }
        for elb in elb_load_balancers['LoadBalancerDescriptions']
    ]

# Function to get ELBv2 load balancers
def get_elbv2_load_balancers(region):
    elbv2_load_balancers = run_aws_command(['aws', 'elbv2', 'describe-load-balancers', '--region', region])
    return [
        {
            'ResourceType': 'Elastic Load Balancer v2',
            'ResourceId': elb['LoadBalancerArn'],
            'ResourceName': elb['LoadBalancerName']
        }
        for elb in elbv2_load_balancers['LoadBalancers']
    ]

# Function to get NAT Gateways
def get_nat_gateways(region):
    nat_gateways = run_aws_command(['aws', 'ec2', 'describe-nat-gateways', '--region', region])
    return [
        {
            'ResourceType': 'NAT Gateway',
            'ResourceId': nat_gw['NatGatewayId'],
            'ResourceName': 'N/A'  # NAT Gateways don't have a name tag by default
        }
        for nat_gw in nat_gateways['NatGateways']
    ]

# Function to get Elastic IPs
def get_elastic_ips(region):
    elastic_ips = run_aws_command(['aws', 'ec2', 'describe-addresses', '--region', region])
    return [
        {
            'ResourceType': 'Elastic IP',
            'ResourceId': eip['PublicIp'],
            'ResourceName': next(
                (tag['Value'] for tag in eip.get('Tags', []) if tag['Key'] == 'Name'), 'N/A'
            )
        }
        for eip in elastic_ips['Addresses']
    ]

# Main function to parse arguments and run the script
def main():
    parser = argparse.ArgumentParser(description="List AWS resources with their names.")
    parser.add_argument('--region', required=True, help="AWS region name")
    
    args = parser.parse_args()

    all_resources = []

    all_resources.extend(get_ec2_instances(args.region))
    all_resources.extend(get_ebs_volumes(args.region))
    all_resources.extend(get_elb_load_balancers(args.region))
    all_resources.extend(get_elbv2_load_balancers(args.region))
    all_resources.extend(get_nat_gateways(args.region))
    all_resources.extend(get_elastic_ips(args.region))

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

if __name__ == "__main__":
    main()
