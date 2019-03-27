## Summary
This directory offers sample codes which consist of lambda function with lambda layer.  
To deploy on aws cloud, aws sam is used.  
These can deploy by executing the deploy.sh.

## Directory Structure
```
- logger/            # Logging library uploaded on lambda layer.
- aws-sam.yaml       # AWS SAM template.
- deploy.sh          # Shell script for deploying on aws cloud with aws cli.
- lambda_handler.py  # Lambda function's entry point.
```