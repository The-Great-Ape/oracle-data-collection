from solana.publickey import PublicKey        
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
import json
import pandas as pd

solana_client = Client('https://explorer-api.mainnet-beta.solana.com/')

def kwargparse(kwargs: dict):
    # Parses keyword arguments

    params = ""
    request = ""
    for key, value in kwargs.items():
        if key == 'params':
            params = value
        elif key == 'request':
            request = value
        else:
            print("Invalid argument.")
            return None
    if params != "" and request == "":
        return params, "Exclude"
    elif request != "" and params == "":
        return "Exclude", request
    elif params != "" and request != "":
        return params, request
    
def reqparse(response: list or dict, request: list):
    # Selects and returns a new list[dict] with only desired data
    
    if type(response) == dict:
        listrep = response
        response = []
        response.append(listrep)

    selected_response = []
    for resp in response:
        selected = {}
        for key in request:
            if key.find('.') != -1:
                key = key.split('.')
                #key = ['account', 'lamports']
                name = key[0]
                sub = key[1]
                selected[sub] = resp[name][sub]
                continue
                
            selected[key] = resp[key]
        selected_response.append(selected)

    return selected_response
    
def txsigs_from_address(account: str, **kwargs):
    # Returns confirmed signatures for transactions involving an address. 
    # PARAMETERS: pubkey/account, before(optional), limit(optional)
        
    if kwargs:
        params, request = kwargparse(kwargs)
            
    response = solana_client.get_confirmed_signature_for_address2(account)['result']
    
    if kwargs:
        if request != "Exclude":
            selected_response = reqparse(response, request)
            return selected_response
        
    return response
            
def confirmed_tx_info(tx_sig: str, **kwargs):
    # Returns transaction details for a confirmed transaction.
    # PARAMETERS: tx_sig, encoding(optional)
        
    if kwargs:
        params, request = kwargparse(kwargs)
        
    response = solana_client.get_confirmed_transaction(tx_sig)['result']
        
    if kwargs:
        if request != "Exclude":
            selected_response = reqparse(response, request)
            return selected_response
        
    return response
    
def acc_info(pubkey: str, **kwargs):
    # Returns account info for the specified public key.
    # PARAMETERS: pubkey, commitment(optional), encoding(optional)

    if kwargs:
        params, request = kwargparse(kwargs)
  
    response = solana_client.get_account_info(pubkey)['result']['value']

    if kwargs:
        if request != "Exclude":
            selected_response = reqparse(response, request)
            return selected_response

    return response
   
def get_bals(pubkey: str, **kwargs):
    # Returns the balance of the account of provided Pubkey.
    # PARAMETERS: pubkey, commitment(optional)

    if kwargs:
        params, request = kwargparse(kwargs)
            
    response = solana_client.get_balance(pubkey)['result']['value']
        
    if kwargs:
        if request != "Exclude":
            selected_response = reqparse(response, request)
            return selected_response
    
    return response

def token_accs_by_owner(pubkey: str, progid: str, **kwargs):
    # Returns all SPL Token accounts by token owner.
    # PARAMETERS: pubkey, opt, commitment(optional)
    # 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
    
    if kwargs:
        params, request = kwargparse(kwargs)
    
    response = solana_client.get_token_accounts_by_owner(pubkey, TokenAccountOpts(program_id=progid))['result']['value']
    
    if kwargs:
        if request != "Exclude":
            selected_response = reqparse(response, request)
            return selected_response
    
    return response
