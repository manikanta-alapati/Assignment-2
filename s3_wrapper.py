import json

class s3_wrapper():

    sample_file = "sample.json"

    def __init__(self, client, bucket_name):
        self.bucket_name = bucket_name
        self.client = client
    
    def download(self, filename, filepath):
        self.client.download_file(self.bucket_name, filename, filepath)
    
    def upload(self, filepath, filename):
        self.client.upload_file(filepath, self.bucket_name, filename)

    def list_files(self):
        return self.client.list_objects(Bucket=self.bucket_name).get("Contents", [])

    def delete(self, filename):
        self.client.delete_object(Bucket=self.bucket_name, Key = filename)

    def read(self, filename):
        self.download(filename, self.sample_file)
        file = open(self.sample_file, "r")
        content = file.read()
        file.close()
        return json.loads(content)
    
    def update(self, filename, json_content):
        file = open(self.sample_file, "w")
        file.write(json.dumps(json_content))
        file.close()
        self.upload(self.sample_file, filename)
    
    def create(self, filename, json_content):
        self.update(filename, json_content)