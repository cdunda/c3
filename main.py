import boto3
import argparse
import sys
from datetime import datetime, timezone


def get_s3_client(use_localstack=False):
    if use_localstack:
        return boto3.client(
            "s3",
            endpoint_url="http://localhost:4566",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
    return boto3.client("s3")


def list_deployments(s3_client, bucket):
    response = s3_client.list_objects_v2(Bucket=bucket, Delimiter="/")
    return [
        prefix["Prefix"].strip("/") for prefix in response.get("CommonPrefixes", [])
    ]


def get_deployment_date(s3_client, bucket, deployment):
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=deployment, MaxKeys=1)
    return response["Contents"][0]["LastModified"]


def delete_deployment(s3_client, bucket, deployment):
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=deployment)
    keys_to_delete = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
    if keys_to_delete:
        s3_client.delete_objects(Bucket=bucket, Delete={"Objects": keys_to_delete})


def main():
    parser = argparse.ArgumentParser(description="Cleanup old deployment folders in S3")
    parser.add_argument("bucket", help="The S3 bucket name")
    parser.add_argument(
        "retain", type=int, help="The number of most recent deployments to retain"
    )
    parser.add_argument(
        "--localstack", action="store_true", help="Use LocalStack for testing"
    )

    parser.add_argument(
        "--min-retain-days",
        type=int,
        default=0,
        help="Minimum number of deployments to retain regardless of age",
    )

    args = parser.parse_args()
    bucket = args.bucket
    retain_count = args.retain
    min_retain_days = args.min_retain_days

    s3_client = get_s3_client(use_localstack=args.localstack)

    deployments = list_deployments(s3_client, bucket)
    deployment_dates = [
        (dep, get_deployment_date(s3_client, bucket, dep)) for dep in deployments
    ]
    deployment_dates.sort(key=lambda x: x[1], reverse=True)

    # Filter deployments older than retain_count
    old_deployments = deployment_dates[retain_count:]

    # Retain minimum number of deployments regardless of age
    if min_retain_days > 0:
        current_date = datetime.now(timezone.utc)
        old_deployments = [
            dep
            for dep in old_deployments
            if (current_date - dep[1]).days > min_retain_days
        ]

    # Delete old deployments
    for dep, _ in old_deployments:
        print(f"Deleting deployment: {dep}")
        delete_deployment(s3_client, bucket, dep)


if __name__ == "__main__":
    main()
