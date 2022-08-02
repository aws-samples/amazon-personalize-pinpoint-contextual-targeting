import json
import boto3
import csv
import time
import os
import re

from urllib.parse import urlparse


client = boto3.client("s3")


def lambda_handler(event, context):
    parsed_uri = urlparse(event.get("jobOutputFile"))
    s3_object = client.get_object(
        Bucket=parsed_uri.netloc, Key=parsed_uri.path[1:])

    s3_content = s3_object["Body"].read().decode("utf-8")

    for item in s3_content.split("\n"):
        if item:
            json_content = json.loads(item.strip())

            recommendedusers = json_content["output"]["usersList"]
            if "itemAttributes" in json_content["input"]:
                itemAttributes = json_content["input"]["itemAttributes"]
                file_name = re.sub("[^A-Za-z]", "", itemAttributes) + "_" + \
                    time.strftime("%Y%m%d-%H%M%S")
            else:
                itemAttributes = json_content["input"]["itemId"]
                file_name = "item_" + itemAttributes + "_" + \
                    time.strftime("%Y%m%d-%H%M%S")

    return {
        "segmentName": file_name,
        "users": recommendedusers
    }
