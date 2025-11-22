import boto3
from app.config import settings

client = boto3.client("lambda", region_name=settings.AWS_REGION)

def run_code(payload):
    response = client.invoke(
        FunctionName=settings.AWS_LAMBDA_FUNCTION,
        Payload=str.encode(str(payload))
    )
    return eval(response["Payload"].read().decode())
