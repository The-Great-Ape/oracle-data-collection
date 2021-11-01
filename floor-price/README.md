#### Completion / Todo

* SolanArt and AlphaArt price fetchers have been completed, the prices were found in transaction metadatas. 
* For SolanArt, this was found in the memo of the 'get_confirmed_signature_for_address2' RPC call.
* For AlphaArt, this was found in the meta[logmessages[]] of the 'get_confirmed_transaction' RPC call.

 We **need** to identify where we can find this for:

* Digital Eyes Escrow F4ghBzHFNgJxV4wEQDchU5i7n4XWWMBSaq7CuswGiVsr
* Magic Eden GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp
* FTX Marketplace 73tF8uN3BwVzUzwETv59WNAafuEBct2zTgYbYXLggQiU
* SMB Market G6xptnrkj4bxg9H9ZyPzmAnNsGghSxZ7oBCL1KNKJUza

The possibility of this is unclear - reached out to the aforementioned marketplaces supports/discords for direction.

Data from SMB's website could be easily scraped, and FTX has an API available. However - ideally, we want to obtain this data on-chain.
