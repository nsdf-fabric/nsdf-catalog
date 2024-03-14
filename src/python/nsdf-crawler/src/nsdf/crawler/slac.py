import boto3
from botocore.client import Config
import csv


def write_csv(filename, rows):
    """
    :param filename: name to create the file
    :param rows: list of objects
    """
    with open(filename, "wt") as f:
        csv.writer(f).writerows(rows)


def get_files_on_s3_resource(bucket_name, folder_path):
    s3 = boto3.resource(
        "s3",
        endpoint_url="https://%s" % "maritime.sealstorage.io/api/v0/s3",
        aws_access_key_id="any",
        aws_secret_access_key="any",
        config=Config(signature_version="s3v4"),
        verify=False,
    )
    bucket = s3.Bucket(bucket_name)
    folder_objects = list(bucket.objects.filter(Prefix=folder_path))
    reformat_objects = []
    for file in folder_objects:
        reformat_objects.append(
            [
                "SLAC",
                bucket.name,
                file.key,
                file.size,
                file.last_modified,
                file.e_tag,
            ]
        )
    return reformat_objects


if __name__ == "__main__":
    data = get_files_on_s3_resource("utah", "supercdms-data/CDMS/UMN/")
    write_csv("slac.csv", data)
