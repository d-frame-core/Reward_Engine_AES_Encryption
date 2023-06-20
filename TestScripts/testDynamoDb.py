import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = dynamodb.Table("IPFS_USER-CID")
# table.delete()
# table = dynamodb.create_table(
#     TableName='IPFS_USER-CID',
#     KeySchema=[
#         {
#             'AttributeName': 'UserPublicAddress',
#             'KeyType': 'HASH'
#         },
#             {
#             'AttributeName': 'IpfsCid',
#             'KeyType': 'RANGE'
#         },
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'UserPublicAddress',
#             'AttributeType': 'S'
#         },
#         {
#             'AttributeName': 'IpfsCid',
#             'AttributeType': 'S'
#         },
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 50,
#         'WriteCapacityUnits': 50
#     }
# )

# try:
#     output = table.put_item(
#         Item={
#             "UserPublicAddress": "95u74yr87y87y84yfhhfb",
#             "DeployedDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
#             "IpfsCid": "85875783957758975895898695888888ddddddddddddddddddddddddddddddddddf"
#     }
#     )

#     status_code = output["ResponseMetadata"]["HTTPStatusCode"]
#     if(status_code == 200):
#         print("Record entered to DynamoDB successfully")
#     else:
#         print("Error Occur During Record Insertion")

# except Exception as e:
#         print(f"An error occurred: {str(e)}")

response = table.query(
    KeyConditionExpression=Key('UserPublicAddress').eq('0xA0D4594DC85b492dfAc756C6D4f6398e3a005767')
)
items = response['Items']
for item in items:
    print(item['IpfsCid'])

# response = table.get_item(
#     Key={
#         'UserPublicAddress': '95u74yr87y87y84yfhhfb',
#     }
# )
# item = response['Item']
# print(item)


# Wait until the table exists.
# table.wait_until_exists()

# # # Print out some data about the table.
# print(table.item_count)
# print(list(dynamodb.tables.all()))