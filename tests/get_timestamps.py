import boto3

# Configure boto3 to use the localstack endpoint
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",  # for localstack
    aws_secret_access_key="test",  # for localstack
)

bucket_name = "test-bucket"

response = s3_client.list_objects_v2(Bucket=bucket_name)

if "Contents" in response:
    for obj in response["Contents"]:
        key = obj["Key"]
        object_attributes = s3_client.get_object_attributes(
            Bucket=bucket_name, Key=key, ObjectAttributes=["LastModified"]
        )
        last_modified = object_attributes["LastModified"]
        print(f"File: {key}, LastModified: {last_modified}")
else:
    print("Bucket is empty or doesn't exist.")
