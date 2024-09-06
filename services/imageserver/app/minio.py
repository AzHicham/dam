from minio import Minio


class MinioClient:
    def __init__(self, endpoint, bucket, access_key, secret_key, secure=False):
        self.bucket = bucket
        print(f"Connecting to Minio at {endpoint} with access_key={access_key} and secret_key={secret_key}")
        self.client = Minio(endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        # Create bucket if it does not exist
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload(self, object_name, file_path):
        self.client.fput_object(self.bucket, object_name, file_path)

    def download(self, object_name, file_path):
        self.client.fget_object(self.bucket, object_name, file_path)

    def list_objects(self):
        return self.client.list_objects(self.bucket)

    def remove_object(self, object_name):
        self.client.remove_object(self.bucket, object_name)

