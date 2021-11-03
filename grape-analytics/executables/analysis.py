import pandas as pd
from statistics import median, mode
from wrapper import get_bals, token_accs_by_owner, acc_info
from datetime import date
from solana.rpc.api import Client
import json

def preformat(df):
    col1 = df.columns[0]
    col2 = df.columns[1]
    df.rename(columns = {col1:'pubkey', col2:'nft_count'}, inplace = True)
    df.loc[-1] = [col1, float(col2)]
    df.index = df.index + 1
    df = df.sort_index()
    return df

def add_lamports(df):
    df['lamports'] = None
    for i in range(len(df)):
        pubkey = df['pubkey'][i]
        balance = get_bals(df['pubkey'][i])
        df['lamports'][i] = balance
    return df

# metrics on NFT posession count over all users 
def nft_info(df):
    num = 0
    length = len(df['nft_count'].values)
    for i in range(length):
        num = num + df['nft_count'].values[i]
    nfts_avg = round(num / length)
    nfts_median = median(df['nft_count'].values)
    nfts_mode = mode(df['nft_count'].values)
    
    return nfts_avg, nfts_median, nfts_mode

# metrics on sol/lamport balance over all users
def bal_info(df):
    num = 0
    length = len(df['lamports'].values)
    for i in range(length):
        num = num + df['lamports'].values[i]
    lamports_avg = round(num / length)
    lamports_median = round(median(df['lamports'].values))
    lamports_mode = round(mode(df['lamports'].values))
    sol_avg = round(lamports_avg * 10**-9, 3)
    
    return lamports_avg, lamports_median, lamports_mode, sol_avg

def analyze(df):
    date = pd.to_datetime('today').strftime("%Y/%m/%d")
    no_lamports = preformat(df)
    populated_df = add_lamports(no_lamports)
    nfts_avg, nfts_median, nfts_mode = nft_info(populated_df)
    lamports_avg, lamports_median, lamports_mode, sol_avg = bal_info(populated_df)
    
    nfts_total = 0 
    for val in df['nft_count']:
        nfts_total = nfts_total + val
        
    analytics_dict = {
        'date':[date],
        'users':[len(df)],
        'sol_avg':[sol_avg],
        'lamports_avg':[lamports_avg],
        'lamports_median':[lamports_median],
        'lamports_mode':[lamports_mode],
        'nfts_total':[nfts_total],
        'nfts_avg':[nfts_avg], 
        'nfts_median':[nfts_median],
        'nfts_mode':[nfts_mode]
    }
    
    analytics_df = pd.DataFrame.from_dict(analytics_dict)
    print('done')
    
    return populated_df, analytics_df

def csvsave(array):
    for arr in array:
        folder = arr.split('_')[0]
        files = arr.split(', ')
        for file in files:
            toexec = file + ".to_csv('metrics/" + folder + '/' + file + ".csv')"
            print(toexec)
            exec(toexec)

# Replace names correspondingly
def run():
    smb = pd.read_csv('../csvs/smb.csv')
    aurory = pd.read_csv('../csvs/aurory.csv')
    degens = pd.read_csv('../csvs/degens.csv')
    frakt = pd.read_csv('../csvs/frakt.csv')  
    gecko = pd.read_csv('../csvs/gecko.csv')
    meerkat = pd.read_csv('../csvs/meerkat.csv')
    solsteads = pd.read_csv('../csvs/solsteads.csv')
    stylishstuds = pd.read_csv('../csvs/stylishstuds.csv')
    thugz = pd.read_csv('../csvs/thugz.csv')

    aurory_df, aurory_analytics = analyze(aurory)
    smb_df, smb_analytics = analyze(smb)
    degens_df, degens_analytics = analyze(degens)
    frakt_df, frakt_analytics = analyze(frakt)
    gecko_df, gecko_analytics = analyze(gecko)
    meerkat_df, meerkat_analytics = analyze(meerkat)
    solsteads_df, solsteads_analytics = analyze(solsteads)
    stylishstuds_df, stylishstuds_analytics = analyze(stylishstuds)
    thugz_df, thugz_analytics = analyze(thugz)

    okarray = [
        'aurory_df, aurory_analytics',
        'smb_df, smb_analytics',
        'degens_df, degens_analytics',
        'frakt_df, frakt_analytics',
        'gecko_df, gecko_analytics',
        'meerkat_df, meerkat_analytics',
        'solsteads_df, solsteads_analytics',
        'stylishstuds_df, stylishstuds_analytics',
    'thugz_df, thugz_analytics'
    ]

    csvsave(okarray)
