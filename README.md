# Infrastructure Scripting Challenge

As a member of the Infrastructure team, I want to cleanup old deployment folders in s3 to help manage AWS costs.

Write a script to remove all but the most recent X deployments. The script should take in X as a parameter.

If a deployment is older than X deployments, we will delete the entire folder.

S3 folder bucket assets will look similar to below. 

```json
s3-bucket-name
	deployhash112/index.html
				 /css/font.css
				 /images/hey.png 
	dsfsfsl9074/root.html
				 /styles/font.css
				 /img/hey.png 
  delkjlkploy3/base.html
				 /fonts/font.css
				 /png/hey.png 
  dsfff1234321/...
  klljkjkl123/...
```

## Questions

1. Where should we run this script? 

    I recommend running this script within a lambda. They're cheap and can be run on a cron schedule.

2. How should we test the script before running it production?

    The script should be tested with as close to a real-world example as possible. For example, I have provided a test GitHub Action workflow that will:
    - Leverage LocalStack to mimic S3 API calls.
    - Use Terraform to create a near-real-world environment that can be updated if/when new edge cases arise.

    This approach is useful for iterating locally and verifying prerelease. However, I'd recommended to use more automated verification tests with pytest assertions to decrease toil and reduce human error.

3. If we want to add an additional requirement of deleting deploys older than X days but we must maintain at least Y number of deploys. What additional changes would you need to make in the script?

    There would need to be an additional arg or flag for --min-retain-days
    This could then be used to run another check against the dates to secure any deployments that are slated for deletion by the retain-number alogorithm


## Notes

Write the script in a high-level programming language such as python/nodejs (we prefer python).

Consider using localstack to mimic s3. *Good Idea!*

List any assumptions made in a README.md.
*See [assumptions](./tests/README.md)*

Please provide the github repo of the scripting project.
*You're Here!*


## Solution

### S3 Deployment Cleanup Script

This script cleans up old deployment folders in an S3 bucket, retaining only the most recent X deployments.

### Prerequisites

- This project uses `poetry` for managing virtualenvs and python dependencies
- The script uses `boto3` to interact with AWS S3.
- The tests use `localstack` and `terraform` to create the test deployments

### Install

```sh
poetry install
```

### Usage

```sh
python main.py --help
usage: main.py [-h] [--localstack] [--min-retain-days MIN_RETAIN_DAYS] bucket retain

Cleanup old deployment folders in S3

positional arguments:
  bucket                The S3 bucket name
  retain                The number of most recent deployments to retain

options:
  -h, --help            show this help message and exit
  --localstack          Use LocalStack for testing
  --min-retain-days MIN_RETAIN_DAYS
                        Minimum number of deployments to retain regardless of age
```

#### Example
```sh
python main.py test-bucket 2 --min-retain-days 30
```
This example retains the 2 most recent deployments and deletes deployments older than 30 days.

### Local Testing

#### Set up test env

```sh
terraform -chdir=tests init
terraform -chdir=tests apply -auto-approve
```

#### Cleanup!

```sh
python main.py test-bucket 1 --localstack
```

:cheers: