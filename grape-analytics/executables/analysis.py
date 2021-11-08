import pandas as pd
from statistics import median, mode
from wrapper import get_bals
import math


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
    df['lamports'] = df.pubkey.apply(get_bals)

    return df


# metrics on NFT posession count over all users
def nft_info(df):
    nfts_total = df.nft_count.sum()
    nfts_avg = df.nft_count.mean()

    return nfts_avg, nfts_total


# metrics on sol/lamport balance over all users
def bal_info(df):
    sol_total = round(df.lamports.sum() * 10**-9, 4)
    sol_avg = round(df.lamports.mean() * 10**-9, 4)

    return sol_avg, sol_total


def analyze(csvs):
    results = {}
    for key in list(csvs.keys()):
        df = csvs[key]
        date = pd.to_datetime('today').strftime("%Y/%m/%d")
        no_lamports = preformat(df)
        populated_df = add_lamports(no_lamports)
        nfts_avg, nfts_total = nft_info(populated_df)
        sol_avg, sol_total = bal_info(populated_df)

        analytics_dict = {
            'community':[key],
            'date':[date],
            'users':[len(df)],
            'sol_avg':[sol_avg],
            'sol_total':[sol_total],
            'nfts_avg':[nfts_avg],
            'nfts_total':[nfts_total]
        }

        analytics_df = pd.DataFrame.from_dict(analytics_dict)
        analytics_df = analytics_df.set_index('community')
        result = [populated_df, analytics_df]
        results[key] = result

    return results


def scores(csvs):
    for key in list(csvs.keys()):
        df = csvs[key][1]
        users = df['users'].values[0]
        nftnum = df['nfts_total'].values[0]
        while True:
            print("For community: ", key)

            holders = input("Number Of Holders: ")
            try:
                int(holders)
                break
            except:
                print("Invalid entry. Passing NaN.")
                holders = math.nan
                break
            supply = input("Number of NFT Supply: ")
            try:
                int(supply)
                break
            except:
                print("Invalid entry. Passing NaN.")
                supply = math.nan
                break
            floor = input("Floor price: ")
            try:
                int(floor)
                break
            except:
                print("Invalid entry. Passing NaN.")
                floor = math.nan
                break

        user_gscore = float(users) / float(holders)
        nft_gscore = float(nftnum) / float(supply)
        nft_floor = float(floor) * float(supply)

        df['user_grape_score'] = str(round(user_gscore * 100, 2)) + '%'
        df['nft_grape_score']  = str(round(nft_gscore * 100, 2)) + '%'
        df['nft_floor']  = str(round(nft_floor, 3)) + ' SOL'


    return df


def leaderboard(csvs):
    usernum = {}
    solavg = {}
    soltotal = {}
    nftsavg = {}
    nftstotal = {}
    nftgrapescore = {}
    usergrapescore = {}
    floorprice = {}
    for key in list(csvs.keys()):
        df = csvs[key][1]
        name = df.index.values[0]
        usernum[name] = df['users'].values[0]
        solavg[name] = df['sol_avg'].values[0]
        soltotal[name] = df['sol_total'].values[0]
        nftsavg[name] = df['nfts_avg'].values[0]
        nftstotal[name] = df['nfts_total'].values[0]
        nftgrapescore[name] = df['nft_grape_score'].values[0]
        usergrapescore[name] = df['user_grape_score'].values[0]
        floorprice[name] = df['nft_floor'].values[0]

    userdf = pd.DataFrame(usernum, index=['Users'])
    solavgdf = pd.DataFrame(solavg, index=['Sol Average'])
    totsoldf = pd.DataFrame(soltotal, index=['Sol Total'])
    nftsavgdf = pd.DataFrame(nftsavg, index=['NFTs Average'])
    totnftsdf = pd.DataFrame(nftstotal, index=['NFTs Total'])
    nftgrapescoredf = pd.DataFrame(nftgrapescore, index=['NFT Grape Score'])
    usergrapescoredf = pd.DataFrame(usergrapescore, index=['User Grape Score'])

    return [userdf, solavgdf, totsoldf, nftsavgdf, totnftsdf, nftgrapescoredf, usergrapescoredf]


def leaderboard_save(csvs):
    for csv in csvs:
        filename = "../metrics/leaderboards/" + csv.index.values[0] + ".csv"
        csv.to_csv(filename)


# Replace names correspondingly
def run():
    # paths = [
    #    "../csvs/smb.csv",
    #    "../csvs/aurory.csv",
    #    "../csvs/degens.csv",
    #    "../csvs/frakt.csv",
    #    "../csvs/gecko.csv",
    #    "../csvs/meerkat.csv",
    #    "../csvs/solsteads.csv",
    #    "../csvs/stylishstuds.csv",
    #    "../csvs/thugz.csv",
    # ]
    paths = input("Input file paths: ")
    csvs_preanalysis = csvdict(paths.split(" "))
    print("Preanalysis done.")
    csvs_postanalysis = analyze(csvs_preanalysis)
    print("Analysis done.")
    scores(csvs_postanalysis)
    csvs_leaderboard = leaderboard(csvs_postanalysis)
    leaderboard_save(csvs_leaderboard)
