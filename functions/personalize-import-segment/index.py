import boto3
import csv
import os


client = boto3.client("s3")
segment_import_bucket = os.environ.get("SEGMENT_IMPORT_BUCKET")
segment_import_prefix = os.environ.get("SEGMENT_IMPORT_PREFIX")


def lambda_handler(event, context):
    file_name = event.get("segmentName")
    file_path = "/tmp/" + file_name + ".csv"

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Id"])
        for val in event.get("endpoints"):
            writer.writerow([val])
        f.close()

    key = segment_import_prefix + file_name + ".csv"
    client.upload_file(file_path, segment_import_bucket, key)
