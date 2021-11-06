import pandas as pd
from statistics import median, mode
from wrapper import get_bals, token_accs_by_owner, acc_info
from datetime import date
from solana.rpc.api import Client
import json

def csvdict(paths):
    csvs = {}
    for path in paths:
        name = path.split('.')[-2].split('/')[-1]
        df = pd.read_csv(path)
        csvs[name] = df
    return csvs

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
    sol_avg = round(lamports_avg * 10**-9, 4)
    sol_total = round(num * 10**-9, 4)

    return lamports_avg, lamports_median, lamports_mode, sol_avg, sol_total

def analyze(csvdict):
    results = {}
    for key in csvdict.keys:
        df = csvdict[key]
        date = pd.to_datetime('today').strftime("%Y/%m/%d")
        no_lamports = preformat(df)
        populated_df = add_lamports(no_lamports)
        nfts_avg, nfts_median, nfts_mode = nft_info(populated_df)
        lamports_avg, lamports_median, lamports_mode, sol_avg, sol_total = bal_info(populated_df)
        
        nfts_total = 0 
        for val in df['nft_count']:
            nfts_total = nfts_total + val
        
        analytics_dict = {
            'date':[date],
            'users':[len(df)],
            'sol_avg':[sol_avg],
            'sol_total':[sol_total],
            #'lamports_avg':[lamports_avg],
            #'lamports_median':[lamports_median],
            #'lamports_mode':[lamports_mode],
            'nfts_avg':[nfts_avg], 
            'nfts_total':[nfts_total]
            #'nfts_median':[nfts_median],
            #'nfts_mode':[nfts_mode]
        }
    
        analytics_df = pd.DataFrame.from_dict(analytics_dict)
        result = [populated_df, analytics_df]
        
        results[key] = result
    return results

def csvsave(array):
    for arr in array:
        folder = arr.split('_')[0]
        files = arr.split(', ')
        for file in files:
            toexec = file + ".to_csv('metrics/" + folder + '/' + file + ".csv')"
            print(toexec)
            exec(toexec)

def newdfs(dfs):
    usernum = {}
    solavg = {}
    soltotal = {}
    nftsavg = {}
    nftstotal = {}
    grapescore = {}
    for df in dfs:
        print(df)
        name = df['name'].values[0]
        users = df['users'].values[0]
        sol_avg = df['sol_avg'].values[0]
        sol_total = df['sol_total'].values[0]
        nfts_avg = df['nfts_avg'].values[0]
        nfts_total = df['nfts_total'].values[0]
        grape_score = df['grape_score'].values[0]
        usernum[name] = users
        solavg[name] = sol_avg
        soltotal[name] = sol_total
        nftsavg[name] = nfts_avg
        grapescore[name] = grape_score
    
    userdf = pd.DataFrame(usernum, index=[0])
    solavgdf = pd.DataFrame(solavg, index=[0])
    totsoldf = pd.DataFrame(soltotal, index=[0])
    nftsavgdf = pd.DataFrame(nftsavg, index=[0])
    totnftsdf = pd.DataFrame(nftstotal, index=[0])
    grapescoredf = pd.DataFrame(grapescore, index=[0])
    
    return userdf, solavgdf, totsoldf, nftsavgdf, totnftsdf, grapescoredf

# Replace names correspondingly
def run():
    paths = ['../csvs/smb.csv',
       '../csvs/aurory.csv',
       '../csvs/degens.csv',
      '../csvs/frakt.csv',
      '../csvs/gecko.csv',
      '../csvs/meerkat.csv',
      '../csvs/solsteads.csv',
      '../csvs/stylishstuds.csv',
      '../csvs/thugz.csv']

    csvs = csvdict(paths)
    results = analyze(csvs)
    analyses = []
    for key in results.keys():
        csv = results[key]
        analyses.append(csv)

    csvsave(analyses)
