import boto3
from botocore.config import Config
from botocore import UNSIGNED
import requests
import csv
import json
import os


class OSN:
    def __init__(self, name):
        self.name = name
        self.GET_BUCKETS_URL = "https://osn-api.sdsc.edu/buckets"

    def get_bucket_list(self):
        """
        :return: list of public buckets
        """
        res = requests.get(self.GET_BUCKETS_URL)
        if res.status_code == 200:
            return json.loads(res.content)
        return None

    def get_bucket_details(self, bucket):
        """
        :param bucket: the bucket to be checked
        :return: the response from the head_bucket request
        """

        bucket_prefix = bucket.split(".")[0]
        site = bucket.replace("%s." % bucket_prefix, "")

        s3 = boto3.client(
            "s3",
            endpoint_url="https://%s" % site,
            config=Config(signature_version=UNSIGNED),
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

    def get_object_list(self, bucket, prefix=""):
        """
        :param bucket: the bucket to be checked
        :param prefix: limits the response to keys that begin with the specified prefix
        :return: the response from the list_objects request
        """

        bucket_prefix = bucket.split(".")[0]
        site = bucket.replace("%s." % bucket_prefix, "")
        print(site, bucket_prefix)
        max_keys = self.get_bucket_details(bucket)["object-count"]

        s3 = boto3.client(
            "s3",
            endpoint_url="https://%s" % site,
            config=Config(signature_version=UNSIGNED),
        )

        # Get the list of objects for the bucket
        objects = s3.list_objects_v2(
            Bucket=bucket_prefix, MaxKeys=max_keys, Prefix=prefix
        )["Contents"]

        reformat_objects = []

        # Reformat the response
        for object in objects:
            reformat_objects.append(
                [
                    self.name,
                    bucket,
                    object["Key"],
                    object["Size"],
                    object["LastModified"],
                    object["ETag"],
                ]
            )

        return reformat_objects

    def write_csv(self, filename, rows):
        """
        :param filename: name to create the file
        :param rows: list of objects
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except:
            pass
        with open(filename, "wt") as f:
            csv.writer(f).writerows(rows)


if __name__ == "__main__":
    osn = OSN("OSN")
    buckets_list = osn.get_bucket_list()
    objects = []
    for bucket in buckets_list:
        objects = objects + osn.get_object_list(bucket=bucket)
    osn.write_csv("osn.csv", objects)
