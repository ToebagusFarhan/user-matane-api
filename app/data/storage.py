import os
from google.cloud import storage
import datetime
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
bucket_name = os.environ.get("BUCKET_NAME")

def get_bucket(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    return bucket

def upload_blob_to_folder(source_file_name, destination_folder_name, destination_blob_name):
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(f"{destination_folder_name}/{destination_blob_name}")
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_folder_name}/{destination_blob_name}.")
    

def generate_presigned_url_for_profile(blob_name, expiration=3600):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"userProfile/{blob_name}")
    url = blob.generate_signed_url(expiration=datetime.timedelta(seconds=expiration), method='GET')
    return url

