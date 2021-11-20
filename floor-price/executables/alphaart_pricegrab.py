# REWRITE WITHOUT WRAPPER
from wrapper import token_accs_by_owner, txsigs_from_address, confirmed_tx_info


def alphaart_pricefetch():
    pubkeys = token_accs_by_owner(
        "4pUQS4Jo2dsfWzt3VgHXy3H6RYnEDd11oWPiaM2rdAPw",
        "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
        request=["pubkey"],
    )
    prices = {}
    for pubkey in pubkeys:
        address = pubkey["pubkey"]
        txsig = txsigs_from_address(address)[0]["signature"]
        price_lamports = confirmed_tx_info(txsig)["meta"]["logMessages"][14].split(" ")[
            -1
        ]
        try:
            price = float(price_lamports) * 10 ** -9
        except:
            continue
        prices[address] = price
    return prices
