import os
import boto3
import boto3.session


class DigitalOcean():
    def __init__(self):
        self.session = boto3.session.Session()
        self.aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        self.aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        self.client = self.session.client('s3',
            region_name='nyc3',
            endpoint_url='https://nyc3.digitaloceanspaces.com',
            aws_access_key_id=self.aws_access_key_id[0],
            aws_secret_access_key=self.aws_secret_access_key)

    def upload_to_spaces(self, project_name, data, uri, acl):
        extra_args = { "ACL": acl }
        self.client.put_object(Bucket=project_name, Key=uri, Body=data, **extra_args)
    
    def upload_file(self, src_file, project_name, dest_file, acl):
        self.client.upload_file(Filename=src_file, Bucket=project_name, Key=dest_file, ExtraArgs={ "ACL": acl })
