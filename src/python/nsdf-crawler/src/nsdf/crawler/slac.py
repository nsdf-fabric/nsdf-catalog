"""
NSDF-Catalog: A lightweight indexing service

v0.0.1

`Read the paper here <https://www.computer.org/csdl/proceedings-article/ucc/2022/608700a001/1LvAfybO4OQ>`_

NSDF-Catalog is a lightweight indexing service with minimal metadata that complements existing domain-specific and rich-metadata collections.
NSDF-Catalog is part of the National Science Data Fabric (NSDF) initiative, funded by the National Science Fundation (NSF).
NSDF-Catalog is designed to facilitate multiple related objectives within a flexible microservice to:
(i) coordinate data movements and replication of data from origin repositories within the NSDF federation
(ii) build an inventory of existing scientific data to inform the design of next-generation cyberinfrastructure; and
(iii) provide a suite of tools for discovery of datasets for cross-disciplinary research.
NSDF-Catalog indexes scientific data at a fine-granularity at the file or object level to inform data distribution strategies and to improve the experience for users from the consumer perspective, with the goal of allowing end-toend dataflow optimizations. Index Terms—national science data fabric, scientific data, cloud, high performance computing
"""

import boto3  # Library to connect with S3
from botocore.client import Config  # Library to create a S3 client
import csv  # Library to create a CSV


def write_csv(filename: str, rows: list) -> None:
    """
    :param filename: name to create the file
    :param rows: list of objects

    Return None
    """
    # save the CSV file
    with open(filename, "wt") as f:
        csv.writer(f).writerows(rows)


def get_files_on_s3_resource(bucket_name: str, folder_path: str) -> list:
    """
    :param bucket_name: bucket name
    :param folder_path: folder_path prefix in the bucket

    Return list of objects with the new format
    """
    # create the s3 object
    s3 = boto3.resource(
        "s3",
        endpoint_url="https://%s" % "maritime.sealstorage.io/api/v0/s3",
        aws_access_key_id="any",
        aws_secret_access_key="any",
        config=Config(signature_version="s3v4"),
        verify=False,
    )
    # define a bucket
    bucket = s3.Bucket(bucket_name)
    # search in the list of fodlers
    folder_objects = list(bucket.objects.filter(Prefix=folder_path))
    # obj to count the objects
    reformat_objects = []
    # listing the objects
    for file in folder_objects:
        # creating the list of objects, extracting the metadata
        reformat_objects.append(
            ["slac", bucket.name, file.key, file.size, file.last_modified, file.e_tag]
        )
    # return reformat objects
    return reformat_objects


# main method
if __name__ == "__main__":
    # get d3 data
    data = get_files_on_s3_resource("utah", "supercdms-data/CDMS/UMN/")
    # create the new csv file slac.csv
    write_csv("slac.csv", data)
