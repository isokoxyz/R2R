import os
import boto3
import boto3.session

class DigitalOcean():
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client('s3',
            region_name='nyc3',
            endpoint_url='https://nyc3.digitaloceanspaces.com',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

    def upload_to_spaces(self, data, uri):
        pass
