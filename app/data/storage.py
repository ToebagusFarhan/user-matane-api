import os
import json
from google.cloud import storage
from google.cloud import secretmanager
from google.oauth2 import service_account
import datetime
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

bucket_name = os.getenv("BUCKET_NAME")
project_id = os.getenv("PROJECT_ID")
secret_name = "GOOGLE_APPLICATION_CREDENTIALS" 

# Function to fetch service account key from Secret Manager (Production)
def get_service_account_key_from_secret_manager():
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=secret_path)
    key_data = response.payload.data.decode("UTF-8")
    return json.loads(key_data)

# Function to load service account key locally (for development)
def load_service_account_key_locally():
    key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # Path to the key.json file
    with open(key_path) as key_file:
        return json.load(key_file)

# Function to initialize the Storage client
def get_storage_client():
    if os.getenv("ENVIRONMENT") == "production":
        # In production, fetch the key from Secret Manager
        key_data = get_service_account_key_from_secret_manager()
    else:
        # In local development, load the key from the local environment variable (key file path)
        key_data = load_service_account_key_locally()
    
    credentials = service_account.Credentials.from_service_account_info(key_data)
    client = storage.Client(credentials=credentials, project=credentials.project_id)
    return client

def get_bucket(bucket_name):
    client = get_storage_client()
    bucket = client.get_bucket(bucket_name)
    return bucket

def upload_blob_to_folder(source_file_name, destination_folder_name, destination_blob_name):
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(f"{destination_folder_name}/{destination_blob_name}")
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_folder_name}/{destination_blob_name}.")

def generate_presigned_url_for_profile(blob_name, expiration=3600):
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"userProfile/{blob_name}")
    url = blob.generate_signed_url(expiration=datetime.timedelta(seconds=expiration), method='GET')
    return url
