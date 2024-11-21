import os
from google.cloud import storage
from google.auth import compute_engine
import datetime
from dotenv import load_dotenv
load_dotenv()


bucket_name = os.environ.get("BUCKET_NAME")
service_account = os.environ.get("SERVICE_ACCOUNT")
credentials = compute_engine.Credentials()
project_id = os.environ.get("PROJECT_ID")

def get_bucket(bucket_name):
    client = storage.Client(credentials=credentials, project=project_id)
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
    url = blob.generate_signed_url(version="v4", expiration=datetime.timedelta(seconds=expiration), method='GET', service_account_email=service_account)
    return url

