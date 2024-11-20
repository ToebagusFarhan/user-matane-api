import os
from google.cloud import storage
from flask import jsonify


# Use with utmost fucking caution!!!
# Highly discouraged to use this in production
# This is for testing purposes only
# Please me don't forget to remove this
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

def get_bucket(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    return bucket

def upload_blob_to_folder(bucket_name, source_file_name, destination_folder_name, destination_blob_name):
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(f"{destination_folder_name}/{destination_blob_name}")
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_folder_name}/{destination_blob_name}.")

def generate_signed_url(file_name):
  
    bucket_name = "matane-bucket"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=3600,  # URL valid for 1 hour
        method="GET"
    )

    return jsonify({"signed_url": signed_url})
