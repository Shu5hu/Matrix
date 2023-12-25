# Import your VM as an image

You can use VM Import/Export to import virtual machine (VM) images from your virtualization environment to Amazon EC2 as Amazon Machine Images (AMI), which you can use to launch instances. Subsequently, you can export the VM images from an instance back to your virtualization environment. This enables you to leverage your investments in the VMs that you have built to meet your IT security, configuration management, and compliance requirements by bringing them into Amazon EC2.

## Prerequisites

- Create an Amazon S3 bucket for storing the exported images or choose an existing bucket. The bucket must be in the Region where you want to import your VMs. For more information about S3 buckets, see the [Amazon Simple Storage Service User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html).

- If you have not already installed the AWS CLI on the computer you'll use to run the import commands, see the [AWS Command Line Interface User Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

## Upload the image to Amazon S3

Upload your VM image file to your Amazon S3 bucket using the upload tool of your choice. For information about uploading objects through the Amazon S3 console, see [Uploading Objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html).

## Create an IAM role

VM Import/Export requires a role to perform certain operations on your behalf. You must create a service role named vmimport with a trust relationship policy document that allows VM Import/Export to assume the role, and you must attach an IAM policy to the role.

#### Prerequisite

You must enable AWS Security Token Service (AWS STS) in any Region where you plan to use VM Import/Export. For more information, see Activating and [deactivating AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-activate-deactivate).

#### Create the service role

1. Create a file named `trust-policy.json` on your computer. Add the following policy to the file:
   
```
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Effect": "Allow",
         "Principal": { "Service": "vmie.amazonaws.com" },
         "Action": "sts:AssumeRole",
         "Condition": {
            "StringEquals":{
               "sts:Externalid": "vmimport"
            }
         }
      }
   ]
}
```

2. Use the create-role command to create a role named vmimport and grant VM Import/Export access to it. Ensure that you specify the full path to the location of the trust-policy.json file that you created in the previous step, and that you include the file:// prefix as shown the following example:

```
aws iam create-role --role-name vmimport --assume-role-policy-document "file://C:\path\to\trust-policy.json"
```

3. Create a file named `role-policy.json` with the following policy, where *`disk-image-file-bucket`* is the bucket for disk images and *`disk-image-file-name`* is the name of the exported images:

```
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect": "Allow",
         "Action": [
            "s3:GetBucketLocation",
            "s3:GetObject",
            "s3:ListBucket" 
         ],
         "Resource": [
            "arn:aws:s3:::disk-image-file-bucket",
            "arn:aws:s3:::disk-image-file-bucket/*"
         ]
      },
      {
         "Effect": "Allow",
         "Action": [
            "s3:GetBucketLocation",
            "s3:GetObject",
            "s3:ListBucket",
            "s3:PutObject",
            "s3:GetBucketAcl"
         ],
         "Resource": [
            "arn:aws:s3:::disk-image-file-name",
            "arn:aws:s3:::disk-image-file-name/*"
         ]
      },
      {
         "Effect": "Allow",
         "Action": [
            "ec2:ModifySnapshotAttribute",
            "ec2:CopySnapshot",
            "ec2:RegisterImage",
            "ec2:Describe*"
         ],
         "Resource": "*"
      }
   ]
}
```

4. Use the following put-role-policy command to attach the policy to the role created above. Ensure that you specify the full path to the location of the `role-policy.json` file.

```
aws iam put-role-policy --role-name vmimport --policy-name vmimport --policy-document "file://C:\path\to\role-policy.json"
```

## Import the VM

After you upload your VM image file to Amazon S3, you can use the AWS CLI to import the image. These tools accept either the Amazon S3 bucket and path to the file or a URL for a public Amazon S3 file.

- Import an image with a single disk

The following is an example `containers.json` file that specifies the image using an S3 bucket, where *`disk-image-file-bucket`* is the bucket for disk images and *`disk-image-file-name`* is the name of the exported images:

```
[
  {
    "Description": "My Server OVA",
    "Format": "ova",
    "UserBucket": {
        "S3Bucket": "disk-image-file-bucket",
        "S3Key": "disk-image-file-name"
    }
  }
]
```

The following is an example `containers.json` file that specifies the image using a URL in Amazon S3.

```
[
  {
    "Description": "My Server OVA",
    "Format": "ova",
    "Url": "s3://my-import-bucket/vms/my-server-vm.ova"
  }
]
```

- Import an image with multiple disks

The following is an example `containers.json file`.

```
[
  {
    "Description": "First disk",
    "Format": "vmdk",
    "UserBucket": {
        "S3Bucket": "my-import-bucket",
        "S3Key": "disks/my-server-vm-disk1.vmdk"
    }
  },          
  {
    "Description": "Second disk",
    "Format": "vmdk",
    "UserBucket": {
        "S3Bucket": "my-import-bucket",
        "S3Key": "disks/my-server-vm-disk2.vmdk"
    }
  }
]
```

---


Use the following command to import an image with a single disk.

```
aws ec2 import-image --region <region> --description "<description>" --disk-containers "file://C:\path\to\containers.json"
```

## Monitor an import image task

Use the describe-import-image-tasks command to return the status of an import task, The `import-ami-xxxx` value you can get from the output of the last command.

```
aws ec2 describe-import-image-tasks --import-task-ids import-ami-xxxxxx
```

Status values include the following:

- `active` — The import task is in progress.
- `deleting` — The import task is being canceled.
- `deleted` — The import task is canceled.
- `updating` — Import status is updating.
- `validating` — The imported image is being validated.
- `validated` — The imported image was validated.
- `converting` — The imported image is being converted into an AMI.
- `completed` — The import task is completed and the AMI is ready to use.

* *You can use tools like `watch` to see the progress of the creation process, this process takes a few minutes*

After the import image task is completed, the output includes the ID of the AMI. The following is example output that includes ImageId.

    {
        "ImportImageTasks": [
            {
                "ImportTaskId": "import-ami-xxxxxxxx",
                "ImageId": "ami-1234567890EXAMPLE",
                "SnapshotDetails": [
                    {
                        "DiskImageSize": 705638400.0,
                        "Format": "ova",
                        "SnapshotId": "snap-111222333444aaabb"
                        "Status": "completed",
                        "UserBucket": {
                            "S3Bucket": "my-import-bucket",
                            "S3Key": "vms/my-server-vm.ova"
                        }
                    }
                ],
                "Status": "completed"
            }
        ]
    }

## Cancel an import image task

If you need to cancel an active import task, use the cancel-import-task command.

```
aws ec2 cancel-import-task --import-task-id import-ami-xxxxxxx
```

## Next steps

After the import image task is complete, you can launch an instance using the resulting AMI or copy the AMI to another Region.

Use the following command to copy your imported AMI to new region or create on the same region with new name

```
aws ec2 copy-image --source-image-id <ami-xxxxx> --source-region <source region> --region <new region> --name <new-name> --description "<description>"
```

After that completes successfully, you can remove the original AMI with:

```
aws ec2 deregister-image --image-id <ami-xxxxx>
```