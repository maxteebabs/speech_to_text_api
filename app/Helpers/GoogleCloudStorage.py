import logging
import os
import cloudstorage as gcs
from google.cloud import storage
# import webapp2

# from google.appengine.api import app_identity
class GoogleCloudStorage:
    bucket_name = ""
    storage_client = None
    def __init__(self): 
        self.bucket_name = os.environ.get("BUCKET_NAME")
        self.storage_client = storage.Client()
    def createBucket(self, bucket_name):
        bucket = self.storage_client.create_bucket(bucket_name)
        print("Bucket {} created.".format(bucket.name))
    def getBucketName(self):
        # bn = app_identity.get_default_gcs_bucket_name()
        bucket = self.storage_client.get_bucket(self.bucket_name)
        return bucket
    def store(self, filename, content_type):
        return self.upload_blob(self.bucket_name, filename, content_type)

    def upload_blob(self, bucket_name, source_file_name, content_type="audio/mpeg"):
        """Uploads a file to the bucket."""
        # bucket_name = "your-bucket-name"
        # source_file_name = "local/path/to/file"
        # destination_blob_name = "storage-object-name"
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(source_file_name)
        blob.upload_from_filename(source_file_name, content_type=content_type)
        filepath = "gs://{}/{}".format(bucket_name,source_file_name)
        return filepath

    def list_blobs(self, bucket_name):
        """Lists all the blobs in the bucket."""
        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = self.storage_client.list_blobs(bucket_name)

        for blob in blobs:
            print(blob.name)

    def delete_file(self, filename):
        """Delete file from GCP bucket."""
        bucket = self.storage_client.bucket(self.bucket_name)
        bucket.delete_blob(filename)

    def rename_file(self, filename, newfilename):
        """Rename file in GCP bucket."""
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(filename)
        bucket.rename_blob(blob,
                        new_name=newfilename)
        # return f'{fileName} renamed to {newFileName}.'
        
