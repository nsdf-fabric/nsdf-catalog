import boto3
from botocore.client import Config

config = Config(signature_version="s3v4")
# s3 = boto3.resource(
#     "s3",
#     endpoint_url="https://maritime.sealstorage.io/api/v0/s3",
#     aws_access_key_id="any",
#     aws_secret_access_key="any",
#     config=config,
#     verify=False,
# )
# bucket = s3.Bucket("utah")


def get_bucket_details(bucket):
    """
    :param bucket: the bucket to be checked
    :return: the response from the head_bucket request
    """

    bucket_prefix = bucket.split(".")[0]
    site = bucket.replace("%s." % bucket_prefix, "")

    s3 = boto3.client(
        "s3",
        endpoint_url="https://maritime.sealstorage.io/api/v0/s3",
        aws_access_key_id="any",
        aws_secret_access_key="any",
        config=config,
        verify=False,
    )
    response = s3.head_bucket(Bucket=bucket_prefix)

    return {
        "bucket": bucket,
        "name": bucket_prefix,
        "site": site,
        "bytes-used": int(
            response["ResponseMetadata"]["HTTPHeaders"]["x-rgw-bytes-used"]
        ),
        "object-count": int(
            response["ResponseMetadata"]["HTTPHeaders"]["x-rgw-object-count"]
        ),
    }


def get_object_list(bucket, prefix=""):
    """
    :param bucket: the bucket to be checked
    :param prefix: limits the response to keys that begin with the specified prefix
    :return: the response from the list_objects request
    """

    bucket_prefix = bucket.split(".")[0]
    site = bucket.replace("%s." % bucket_prefix, "")
    print(site, bucket_prefix)
    max_keys = get_bucket_details(bucket)["object-count"]

    s3 = boto3.resource(
        "s3",
        endpoint_url="https://maritime.sealstorage.io/api/v0/s3",
        aws_access_key_id="any",
        aws_secret_access_key="any",
        config=config,
        verify=False,
    )

    # Get the list of objects for the bucket
    objects = s3.list_objects_v2(Bucket=bucket_prefix, MaxKeys=max_keys, Prefix=prefix)[
        "Contents"
    ]

    reformat_objects = []

    # Reformat the response
    for object in objects:
        reformat_objects.append(
            [
                "SLAC",
                bucket,
                object["Key"],
                object["Size"],
                object["LastModified"],
                object["ETag"],
            ]
        )

    return reformat_objects


print(get_object_list("utah"))
