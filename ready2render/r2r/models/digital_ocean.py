import os
import boto3
import boto3.session


class DigitalOcean():
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client('s3',
            region_name='nyc3',
            endpoint_url='https://nyc3.digitaloceanspaces.com',
            aws_access_key_id=os.getenv(
                'AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv(
                'AWS_SECRET_ACCESS_KEY')
            )

    def upload_to_spaces(self, project_name, data, uri):
        bucket = self.get_bucket_for_project(project_name=project_name)
        self.client.put_object(Bucket=bucket,
            Key=uri,
            Body=data,
            ACL='private',
            Metadata={
                'x-amz-meta-my-key': 'your-value'
            }
        )

    def get_bucket_for_project(self, project_name):
        if project_name == 'kadcars':
            return 'kadcars-nft-metadata'
