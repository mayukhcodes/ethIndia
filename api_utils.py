import streamlit as st
from llm import process_crypto_query
import os
import json
from cdp import Cdp, Wallet
from decimal import Decimal
from dotenv import load_dotenv
from crypto import create_sending_wallet, import_existing_wallet, maybe_fund_wallet, send_mass_payout,transfer



receiving_addresses = ["yuga.base.eth"]

# 3. Specify the amount of ETH to send to each address in the variable below.
transfer_amount = Decimal('0.000002')

# Constants
asset_id = "eth"
seed_file_name = "./encrypted_seed.json"
wallet_file_name = "./wallet.json"

def get_api_response(question, session_id, model):

    response = process_crypto_query(question)

    try:
        load_dotenv()  # Load environment variables from .env file

        api_key_name = os.environ.get('CDP_API_KEY_NAME')
        api_key_private_key = os.environ.get('CDP_API_KEY_PRIVATE_KEY')

        if not api_key_name or not api_key_private_key:
            raise ValueError(
                "CDP API Key Name or CDP API Key Private Key is missing")

        # Configure the CDP SDK
        private_key = api_key_private_key.replace('\\n', '\n')
        Cdp.configure(api_key_name, private_key)

        if os.path.exists(seed_file_name) and os.path.exists(wallet_file_name):
            print("Using existing wallet...")
            sending_wallet = import_existing_wallet()
        else:
            # Create a file with seed_file_name and add an empty JSON object to it
            with open(seed_file_name, 'w') as f:
                f.write('{}')
            sending_wallet = create_sending_wallet()




        # maybe_fund_wallet(sending_wallet)
        # send_mass_payout(sending_wallet)

        print("Finished sending mass payouts!")
    except Exception as error:
        print(f"Error in sending mass payouts: {error}")

    
    if(response['Intent']=="GET"):
            balance = sending_wallet.balance(asset_id="eth")
            return {"answer":"Your balance is" +str(balance)+" "+asset_id}
    if(response['Intent']=="SEND"):
            # balance = sending_wallet.balance(asset_id="eth")
            # return {"answer":"Your balance is" +str(balance)+" "+asset_id}
        print(response)
        transferResponse = transfer(sending_wallet,Decimal(response['Value']),str(response['currency']).lower(),str(response['To']).lower().replace(" ",""))

        return {"answer": transferResponse}
    

    


