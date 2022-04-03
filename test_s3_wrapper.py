import unittest
import boto3
import json
from moto import mock_s3
from s3_wrapper import s3_wrapper

@mock_s3
class CompleteTesting(unittest.TestCase):

    def setUp(self):
        self.client = boto3.client('s3')
        self.bucket_name = "dummy"
        self.client.create_bucket(Bucket=self.bucket_name)
        self.test_client = s3_wrapper(self.client, self.bucket_name)

    def test_s3_wrapper_create(self):
        filename = "example"
        filepath = "sample"
        content = "content"
        self.test_client.create(filename, content)
        self.client.download_file(self.bucket_name, filename, filepath)
        file = open(filepath, "r")
        file_content = file.read()
        file_content = json.loads(file_content)
        assert file_content == content

    def test_s3_wrapper_update(self):
        filename = "example"
        filepath = "sample"
        content = "content"
        self.test_client.update(filename, content)
        self.client.download_file(self.bucket_name, filename, filepath)
        file = open(filepath, "r")
        file_content = file.read()
        file_content = json.loads(file_content)
        assert file_content == content

    def test_s3_wrapper_read(self):
        filename = "example"
        filepath = "sample"
        content = "content"
        self.test_client.create(filename, content)
        self.client.download_file(self.bucket_name, filename, filepath)
        file = open(filepath, "r")
        file_content = file.read()
        file_content = json.loads(file_content)
        read_content = self.test_client.read(filename)
        assert file_content == read_content
            
    def test_s3_wrapper_delete(self):
        filename = "example"
        filepath = "sample"
        content = "content"
        self.test_client.create(filename, content)
        files = list(map(lambda x: x["Key"], self.test_client.list_files()))
        self.test_client.delete(filename)
        files = list(map(lambda x: x["Key"], self.test_client.list_files()))
        try:
            files.index(filename)
            assert False
        except Exception as e:
            assert type(e) == ValueError
