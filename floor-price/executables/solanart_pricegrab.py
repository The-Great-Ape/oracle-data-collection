import json
from wrapper import token_accs_by_owner, txsigs_from_address

def solanart_pricefetch():
    pubkeys = token_accs_by_owner('3D49QorJyNaL4rcpiynbuS3pRH4Y7EXEM6v6ZGaqfFGK', 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', request=['pubkey'])
    prices = {}
    for pubkey in pubkeys:
        address = pubkey['pubkey']
        txsigs = txsigs_from_address(address)
        memo = txsigs[0]['memo']
        if memo == None:
            continue
        sigstart = memo.index('{')
        sigend = memo.index('}') + 1
        memo = memo[sigstart:sigend]
        try:
            price_str = json.loads(memo)['price_sol']
            price = float(price_str)
        except:
            continue
        prices[address] = price
    return prices
