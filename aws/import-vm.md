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

1. Create a file named ==trust-policy.json== on your computer. Add the following policy to the file: