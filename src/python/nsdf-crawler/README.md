# Instructions

Install Python prerequisites:

```
python3 -m pip install --upgrade pip

python3 -m pip install \
  materials-commons-api \
  mdf_forge \
  boto3 \
  awscli \
  imageio \
  bs4 \
  Selenium \
  beautifulsoup4 \
  ratelimit \
  zenodopy
```

To upload results on S3 buckets, you need to configure your S3 credentials (see https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html):

```
aws s3 config 
# insert values as needed
```


## Crawled results

All results are available on a public bucket.

To access from a browser just type for example:

```
https://s3.us-west-1.wasabisys.com/nsdf-catalog-crawler/
https://s3.us-west-1.wasabisys.com/nsdf-catalog-crawler/zenodo/zenodo.csv.gz
```

To download a file using for example a terminal:

```
wget https://s3.us-west-1.wasabisys.com/nsdf-catalog-crawler/zenodo/zenodo.csv.gz
```

To list/get objects using AWS cli:

```
# --no-sign-request since it is a public bucket
aws s3 --no-sign-request --endpoint-url=https://s3.us-west-1.wasabisys.com ls s3://nsdf-catalog-crawler/
```


## Arecibo

Data is scraped from HTML pages (link https://www.naic.edu/datacatalog/index.php/datasets/view/)

From a terminal run the scraping and upload results to the cloud:

```
CSV_FILENAME=/tmp/arecibo.csv
python3 arecibo.py ${CSV_FILENAME} 32
aws s3 --endpoint-url <insert_your_endpoint_here> cp ${CSV_FILENAME} s3://nsdf-catalog/arecibo/arecibo.csv
```

## AWS Open Data

See GitHub repo https://github.com/awslabs/open-data-registry.git.

From a terminal run the scraping and upload results to the cloud:
```
OUTPUT_DIR=/tmp/nsdf-catalog/aws
python3 aws_open_data.py ${OUTPUT_DIR}
aws s3 --endpoint-url <insert_your_endpoint_here> sync ${OUTPUT_DIR} s3://nsdf-catalog/aws/
```

# Cyverse

Using Restful API https://de.cyverse.org/terrain/filesystem/paged-directory.


Create a Cyverse User here https://user.cyverse.org/signup.

From a terminal run the scraping and upload results to the cloud:
```
export CYVERSE_USERNAME='<insert-value>'
export CYVERSE_PASSWORD='<insert-value>'

python3 cyverse.py
aws s3 --endpoint-url <insert_your_endpoint_here> cp cyverse.csv s3://nsdf-catalog/cyverse/cyverse.csv
```


## Dataverse

Using Dataverse Restful API `search` (https://guides.dataverse.org/en/latest/api/search.html)
Each requests returns 1000 records.
We search on all public dataverse 58  instances (see `dataverse.py` file for the instances list):

From a terminal run the scraping and upload results to the cloud:
```
python3 dataverse.py json
python3 dataverse.py csv
aws s3 --endpoint-url <insert_your_endpoint_here> cp dataverse.csv s3://nsdf-catalog/dataverse/dataverse.csv
```

## Digital Rocks

Scraping from HTML pages from https://www.digitalrocksportal.org

From a terminal run the scraping and upload results to the cloud:
```
OUTPUT_DIR=/tmp/nsdf-catalog/digital-rocks
python3 digital_rocks.py ${OUTPUT_DIR}
aws s3 --endpoint-url <insert_your_endpoint_here> sync ${OUTPUT_DIR} s3://nsdf-catalog/digital-rocks/
```

## Dryad

Using flat RESTFUL Api api (https://datadryad.org/api/v2/docs/)
NOTE: Anonymous users of the API are limited to 30 requests per minute

From a terminal run the scraping and upload results to the cloud:
```
python3 dryad.py 
aws s3 --endpoint-url <insert_your_endpoint_here> sync dryad.csv s3://nsdf-catalog/dryad/dryad.csv
python3 material_commons.py
```

## Material Commons

Using `materials_commons.api` (https://github.com/materials-commons/materialscommons.org)

Create a personal token for the scraping (https://materialscommons.org/app/accounts/show)

From a terminal run the scraping and upload results to the cloud:
```
export MC_TOKEN=<insert your token here>
export OUTPUT_DIR=/tmp/nsdf-catalog/mc
python3 material_commons.py ${OUTPUT_DIR}
aws s3 --endpoint-url <insert_your_endpoint_here> sync ${OUTPUT_DIR} s3://nsdf-catalog/mc/
```

## Material Data Facility (Globus)

Using `mdf_forge` API (https://github.com/materials-data-facility/forge)

From a terminal run the scraping and upload results to the cloud:
```
export OUTPUT_DIR=/tmp/nsdf-catalog/mdf
python3 material_data_facility.py ${OUTPUT_DIR}
aws s3 --endpoint-url <insert_your_endpoint_here> sync ${OUTPUT_DIR} s3://nsdf-catalog/mdf/
```


## NEON

Using NEON RESTful API (ref https://data.neonscience.org/data-api/endpoints)

From a terminal run the scraping and upload results to the cloud:
```
python3 neon.py
aws s3 --endpoint-url <insert_your_endpoint_here> cp neon.csv s3://nsdf-catalog/neon/neon.csv
```

## Zenodo

using zenodopy client (https://github.com/lgloege/zenodopy).
NOTE: ZENODO Global limit for guest users	60 requests per minute, 2000 requests per hour (==max overall 30 request per 60 seconds)

From a terminal run the scraping and upload results to the cloud:
```
python3 zenodo.py json
python3 zenodo.py csv
aws s3 --endpoint-url <insert_your_endpoint_here> cp zenodo.csv s3://nsdf-catalog/zenodo/zenodo.csv
```

## Others

List:
- OpenVisus:  It is simple a `find -t f /open/visus/directory`. There is no public repo.
- TACC Ranch: It is simple a `find -t f /public/data`. There is no public repo.






