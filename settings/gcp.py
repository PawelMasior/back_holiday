#import os
import time
import random
import json
from google.cloud import storage, bigquery  # , pubsub_v1
from google.oauth2 import service_account
from io import BytesIO

client_GCP = storage.Client()
client_storage = storage.Client()
client_bigquery = bigquery.Client()

name_project = 'holiday-planner'
name_bucket = 'ai-agents-browsers'
name_database = 'app'

def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        return f'Error: {e}'
                    time.sleep(delay + random.uniform(0.1, 1))
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def blobs_clean(agent_folder):
    bucket = client_GCP.bucket(name_bucket)
    blobs = bucket.list_blobs(prefix=f'{agent_folder}/prtscn/')
    for blob in blobs:
        if '.png' in blob.name: blob.delete()

@retry(max_attempts=3, delay=1)
def img_to_bucket(file_source, file_destination):
    bucket = client_GCP.bucket(name_bucket)
    blob = bucket.blob(file_destination)
    blob.upload_from_filename(file_source)
    return blob.public_url

def _upload_blob_json(content, output_file_location):
    bucket = client_storage.get_bucket(name_bucket)
    blob = bucket.blob(output_file_location)
    blob.upload_from_string(
        data=json.dumps(content),
        content_type='application/json'
    )

def _upload_blob_pdf(pdf, blob_name):
    byte_string = pdf.output(dest="S")
    stream = BytesIO(byte_string)
    stream.seek(0)
    bucket = client_storage.get_bucket(name_bucket)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(stream, content_type='application/pdf')
    # pdf_buffer = BytesIO()
    # pdf.output(pdf_buffer)
    # pdf_buffer.seek(0)
    # bucket = client_storage.get_bucket(name_bucket)
    # blob = bucket.blob(blob_name)
    # blob.upload_from_file(pdf_buffer, content_type='application/pdf')    

# from gcp.func import _load_blob_csv, _prep_json, _upload_blob_json, _upload_blob_pdf
# monitor_id = '{}.{}.{}'.format(name_project, 'internal180d', 'monitor')
# name_bucket = 'lotan-general.appspot.com'
# auth_file = 'gcp/lotan-general-alphaimprover.json'
# auth_file = os.path.join('gcp', f'lotan-general-alphaimprover.json')
# credentials = None
# if os.path.isfile(auth_file):
#     credentials = service_account.Credentials.from_service_account_file(
#         auth_file)
# client_storage = storage.Client(credentials=credentials, project=name_project)
# client_bq = bigquery.Client(credentials=credentials, project=name_project)
# @retry(max_attempts=3, delay=1)
# def img_to_bucket(name_bucket, source_file_name, destination_blob_name):
#     bucket = client_GCP.bucket(name_bucket)
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_filename(source_file_name)
#     return blob.public_url
