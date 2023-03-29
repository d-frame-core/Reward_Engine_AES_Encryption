import boto3
from datetime import datetime

def put_item():
    dynamodb_instance = boto3.resource("dynamodb")
    table = dynamodb_instance.Table("IPFS_USER-CID")

    try:
        output = table.put_item(
            Item={
                "UserPublicAddress": "0xsgduygsdbhsdgbs",
                "DeployedDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
                "IpfsCID": "test2@example.com"
            }
        )

        status_code = output["ResponseMetadata"]["HTTPStatusCode"]
        if(status_code == 200):
            print("Record entered to DynamoDB successfully")
        else:
            print("Error Occur During Record Insertion")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

put_item()