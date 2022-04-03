# Techwondoe Assignment 2

## Requirements

- Latest version of docker should be there.

## Steps to setup the project.

1. Clone the project to your local machine.
2. Add credentials ACCESS_KEY, SECRET_ACCESS_KEY, BUCKET_NAME in secret.py module.
3. Open terminal in the project directory and run these commands.

- `docker build . --tag techwondoe:latest`
- `docker run -dp 5000:5000 techwondoe:latest`

## Steps to test the project.

1. Project has to be setup with above instructions.
2. Open terminal in the project directory and run
