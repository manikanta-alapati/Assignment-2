# Techwondoe Assignment 2

## Requirements

- Latest version of docker and git should be pre-installed in your local machine.

## Steps to setup the project.

1. Create IAM user in your AWS account and add a new group with AmazonS3FullAccess permission. 
2. Save the ACCESS_KEY, SECRET_ACCESS_KEY of the user.
3. Create an S3 bucket.
4. Clone the project to your local machine.
5. Add credentials ACCESS_KEY, SECRET_ACCESS_KEY and BUCKET_NAME in Dockerfile.
6. Open terminal in the project directory and run these commands in the given order.

- `docker build . --tag techwondoe_image:latest`
- `docker run -dp 5000:5000 --name techwondoe_container techwondoe_image`

## Steps to test the REST APIs of the project.

1. Make sure to setup the project with the above setup instructions.
2. Open the examples folder in the project directory to see the usage of all apis.
3. To test them with in vscode itself make sure you install the [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or use any HTTP client like Postman to test the APIs.
4. First run the signup api to register, then use login api to get jwt_token and for checking remaining requests place this jwt_token in Authorization header.
5. Every successful request would return 200 http status code or returns a json response.

## Steps to test the code with moto and pytest

1. Make sure to setup the project with the above setup instructions.
2. Now run this command
- `docker exec -it techwondoe_container pytest`

## Checklist of requirements fulfilment for the assignment 2.

- [x] JWT token based API authorization is added
- [x] Creating and modifying JSON files as per the given JSON schema.
- [x] Created apis for CRUD (Create, Read, Update, Delete) operations on JSON files in S3 bucket.
- [x] Used boto3 SDK and moto for testing the code.
- [x] Dockerised the appliation
- [x] Created a FLASK app for building REST APIs. 
