from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver
from datetime import datetime


retry_config = RetryConfig(retry_limit=3)

print("Initializing the driver")

qldb_driver = QldbDriver("IPFSCIDLedger", retry_config=retry_config)

def insert_documents(transaction_executor, aws_ion):
    print("Inserting a document into IPFSCIDLedger")
    transaction_executor.execute_statement(f"INSERT INTO USER_ADDRESS_IPFS_CID ?", aws_ion)

IPFS_CID="xq5xfqxvqtfy44422"

USER_PUBLIC_ADDRESS="xfyatsfxafx7755"

user_meta_data = { 
            'CID': IPFS_CID,
            'DATE': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'User_Public_Address': USER_PUBLIC_ADDRESS
          }

qldb_driver.execute_lambda(lambda x: insert_documents(x, user_meta_data))

print(f"Document with CID ${IPFS_CID} Inserted to USER_ADDRESS_IPFS_CID Table")