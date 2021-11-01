# Solana.py/Solana RPC Wrapper

Current methods:

1) Returns confirmed signatures for transactions involving an address. 
2) Returns transaction details for a confirmed transaction.
3) Returns account info for the specified public key.
4) Returns the balance of the account of provided Pubkey.
5) Returns all SPL Token accounts by token owner.

# Usage:

Via kwargs, the 'request' argument signifies which section of the response you'd like to see.

For sub-elements/nested lists/dicts, use a '.' - within a 'meta' section there may be another list, programID, so that would look like response=['meta.programID'].

If you want the pubkey and lamports of a given response (assuming it's included), that would look like response=['pubkey', 'lamports'].

# Todo:

Implement argument parsing for the RPC call itself, not the response.
