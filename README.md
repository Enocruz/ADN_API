# Installation

This project is setup with Terraform, in order to deploy this code manually into an AWS account, make sure to have installed terraform and AWS CLI:

## AWS CLI

```bash
aws version
```

The output should look something like this:

```bash
aws-cli/2.10.4 Python/3.9.11 Darwin/22.3.0 exe/x86_64 prompt/off
```

## Terraform

```bash
terraform --version
```

```bash
Terraform v1.3.9
on darwin_arm64
```

In the root folder run the following command:

```bash
terraform init
```

## Setup AWS Credentials

For this to work, you need an Access Key and a Secret Key that you can get from the AWS console. To configure AWS CLI run:

```bash
aws configure
```

You will be asked to fill the information:

```bash
AWS Access Key ID [None]: {ACCESS_KEY}
AWS Secret Access Key [None]: {SECRET_KEY}
Default region name [None]: us-west-2
Default output format [None]: json
```

## Python Setup

Make sure that you have python ^3.9 installed.

```bash
python3 --version
```

If you have python installed, create a virtual environment.

```bash
python3 -m venv venv
```

This will create a folder `venv` in the root. Make sure to activate the virtual environment using:

```bash
source venv/bin/activate
```

Once in the virtual environment, install the dependencies:

```bash
pip install -r requirements.txt
```
