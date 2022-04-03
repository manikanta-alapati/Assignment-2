# Techwondoe Assignment 2

## Requirements

- Latest version of docker should be there.

## Steps to setup the project.
1. Create IAM user in your AWS account and add a new group with AmazonS3FullAccess permission. 
2. Save the ACCESS_KEY, SECRET_ACCESS_KEY of the user.
3. Create a S3 bucket.
4. Clone the project to your local machine.
5. Add credentials ACCESS_KEY, SECRET_ACCESS_KEY and BUCKET_NAME in Dockerfile.
6. Open terminal in the project directory and run these commands.

- `docker build . --tag techwondoe:latest`
- `docker run -dp 5000:5000 techwondoe:latest`

## Steps to test the project.

1. Project has to be setup with above instructions.
2. Use HTTP client like Postman to check the APIs.
3. First run the signup api to register, then use login api to get jwt_token and for every checking remaining requests place this jwt_token in Authorization header.

## Checklist for requirements

- [x] JWT token based API authorization is added
- [x] Creating and modifying JSON files as per the given JSON schema.
- [x] Created apis for CRUD (Create, Read, Update, Delete) operations on JSON files in S3 bucket.
- [x] Used boto3 SDK and moto for testing the code.
- [x] Dockerised the appliation
- [x] Created a FLASK app for building REST APIs. 
