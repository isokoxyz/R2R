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
            aws_access_key_id="DO00CUMTJ7ZEQCJHEBD4",
            aws_secret_access_key="VudP+3LoE5JpuT/8R4jDk8RiL55EG5poeqzHNTRH47A")

    def upload_to_spaces(self, project_name, data, uri, acl):
        bucket = self.get_bucket_for_project(project_name=project_name)
        # test = self.client.get_object(Bucket=bucket,Key="./lol.json")
        # print(test)
        self.client.put_object(Bucket=bucket,
            Key=uri,
            Body=data,
            ACL=acl
        )

    def get_bucket_for_project(self, project_name):
        if project_name == 'kadcars':
            return 'kadcars-manifests'
            # return 'kadcars-nft-metadata'
