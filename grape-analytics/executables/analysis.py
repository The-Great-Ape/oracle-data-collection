import pandas as pd
from statistics import median, mode
from wrapper import get_bals
import math
import os

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


def addscores(csvs):
    for key in list(csvs.keys()):
        df = csvs[key][1]
        users = df['users'].values[0]
        nftnum = df['nfts_total'].values[0]
        
        print("For community: ", key)

        holders = input("Number Of Holders: ")
        try:
            int(holders)
        except:
            print("Invalid entry. Passing NaN.")
            holders = math.nan
            pass
       
        supply = input("Number of NFT Supply: ")
        try:
            int(supply)
        except:
            print("Invalid entry. Passing NaN.")
            supply = math.nan
            pass

        floor = input("Floor price: ")
        try:
            float(floor)
        except:
            print("Invalid entry. Passing NaN.")
            floor = math.nan
            pass

        avgprice = input("Average price: ")
        try:
            float(avgprice)
        except:
            print("Invalid entry. Passing NaN.")
            avgprice = math.nan
            pass

        listed = input("Listed tokens: ")
        try:
            float(listed)
        except:
            print("Invalid entry. Passing NaN.")
            listed = math.nan
            pass

        user_gscore = float(users) / float(holders)
        nft_gscore = float(nftnum) / float(supply)
        nft_floor = float(floor) * float(nftnum)
        nft_floor_supply = float(floor) * float(supply)
        floor_value_score = nft_floor / nft_floor_supply
        nft_avg = float(avgprice) * float(nftnum)
        nft_avg_supply = float(avgprice) * float(supply)
        nft_value_score = nft_avg / nft_avg_supply
        listed_supply_score = float(listed) / float(supply)
        
        df['user_grape_score'] = str(round(user_gscore * 100, 2)) + '%'
        df['nft_grape_score']  = str(round(nft_gscore * 100, 2)) + '%'
        df['grape_nft_floor']  = str(round(nft_floor, 3)) + ' SOL'
        df['overall_nft_floor'] = str(round(nft_floor_supply, 3)) + 'SOL'
        df['floor_value_gscore'] = str(round(floor_value_score, 3)) + '%'
        df['grape_nftval_byaverage'] = str(round(nft_avg, 3)) + 'SOL'
        df['overall_nftval_byaverage'] = str(round(nft_avg_supply, 3)) + 'SOL'
        df['nftval_byaverage_gscore'] = str(round(nft_value_score, 3)) + '%'
        df['listed_supply_score'] = str(round(listed_supply_score, 3)) + '%'


def leaderboard(csvs):
    usernum = {}
    solavg = {}
    soltotal = {}
    nftsavg = {}
    nftstotal = {}
    nftgrapescore = {}
    usergrapescore = {}
    gfloorprice = {}
    overallfloor = {}
    floorgrapescore = {}
    grapenftval = {}
    overallnftval = {}
    nftvalgrapescore = {}
    listedsupplyscore = {}

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
        gfloorprice[name] = df['grape_nft_floor'].values[0]
        overallfloor[name] = df['overall_nft_floor'].values[0]
        floorgrapescore[name] = df['floor_value_gscore'].values[0]
        grapenftval[name] = df['grape_nftval_byaverage'].values[0]
        overallnftval[name] = df['overall_nftval_byaverage'].values[0]
        nftvalgrapescore[name] = df['nftval_byaverage_gscore'].values[0]
        listedsupplyscore[name] = df['listed_supply_score'].values[0]

    userdf = pd.DataFrame(usernum, index=['Users'])
    solavgdf = pd.DataFrame(solavg, index=['Sol Average'])
    totsoldf = pd.DataFrame(soltotal, index=['Sol Total'])
    nftsavgdf = pd.DataFrame(nftsavg, index=['NFTs Average'])
    totnftsdf = pd.DataFrame(nftstotal, index=['NFTs Total'])
    nftgrapescoredf = pd.DataFrame(nftgrapescore, index=['NFT Grape Score'])
    usergrapescoredf = pd.DataFrame(usergrapescore, index=['User Grape Score'])
    floorpricedf = pd.DataFrame(gfloorprice, index=['Grape Floor Price'])
    overallfloordf = pd.DataFrame(overallfloor, index=['Total Floor Price'])
    floorgrapescoredf = pd.DataFrame(floorgrapescore, index=['Floor Grape Score'])
    grapenftval = pd.DataFrame(grapenftval, index=['Grape NFT Value'])
    overallnftval = pd.DataFrame(overallnftval, index=['Overall NFT Value'])
    nftvalgrapescore = pd.DataFrame(nftvalgrapescore, index=['NFT Value Grape Score'])
    listedsupplyscoredf = pd.DataFrame(listedsupplyscore, index=['Listed divby Overall Supply'])

    return [userdf, solavgdf, totsoldf, nftsavgdf, totnftsdf, 
            nftgrapescoredf, usergrapescoredf, floorpricedf, overallfloordf,
            floorgrapescoredf, grapenftval, overallnftval, nftvalgrapescore, listedsupplyscoredf]


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
    #paths = input("Input file paths: ")
    #csvs_preanalysis = csvdict(paths.split(" "))
    
    paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk('../csvs/') for f in filenames if os.path.splitext(f)[1] == '.csv']
    csvs_preanalysis = csvdict(paths)
    print("Preanalysis done.")
    csvs_postanalysis = analyze(csvs_preanalysis)
    print("Analysis done.")
    addscores(csvs_postanalysis)
    csvs_leaderboard = leaderboard(csvs_postanalysis)
    leaderboard_save(csvs_leaderboard)

run()
