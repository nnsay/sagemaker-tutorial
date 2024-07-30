import boto3

# 创建 S3 客户端
s3_client = boto3.client("s3")

# 列出存储桶中的所有对象
bucket_name = "sandbox-sagemaker"
response = s3_client.list_objects_v2(Bucket=bucket_name)

# 打印对象键
if "Contents" in response:
    for obj in response["Contents"]:
        print(obj["Key"])
else:
    print("Bucket is empty.")
