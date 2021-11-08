import pandas as pd
from statistics import median, mode
from wrapper import get_bals
import math


def csvdict(paths):
    csvs = {}
    for path in paths:
        name = path.split(".")[-2].split("/")[-1]
        df = pd.read_csv(path)
        csvs[name] = df
    return csvs


def preformat(df):
    col1 = df.columns[0]
    col2 = df.columns[1]
    df.rename(columns={col1: "pubkey", col2: "nft_count"}, inplace=True)
    df.loc[-1] = [col1, float(col2)]
    df.index = df.index + 1
    df = df.sort_index()
    return df


def add_lamports(df):
    df["lamports"] = None
    for i in range(len(df)):
        balance = get_bals(df["pubkey"][i])
        df["lamports"][i] = balance
    return df


# metrics on NFT posession count over all users
def nft_info(df):
    num = 0
    length = len(df["nft_count"].values)
    for i in range(length):
        num = num + df["nft_count"].values[i]
    nfts_avg = round(num / length)
    nfts_median = median(df["nft_count"].values)
    nfts_mode = mode(df["nft_count"].values)

    nfts_total = 0
    for val in df["nft_count"]:
        nfts_total = nfts_total + val

    return nfts_avg, nfts_total, nfts_median, nfts_mode


# metrics on sol/lamport balance over all users
def bal_info(df):
    num = 0
    length = len(df["lamports"].values)
    for i in range(length):
        num = num + df["lamports"].values[i]
    lamports_avg = round(num / length)
    lamports_median = round(median(df["lamports"].values))
    lamports_mode = round(mode(df["lamports"].values))
    sol_avg = round(lamports_avg * 10 ** -9, 4)
    sol_total = round(num * 10 ** -9, 4)

    return lamports_avg, lamports_median, lamports_mode, sol_avg, sol_total


def analyze(csvs):
    results = {}
    for key in list(csvs.keys()):
        df = csvs[key]
        date = pd.to_datetime("today").strftime("%Y/%m/%d")
        no_lamports = preformat(df)
        populated_df = add_lamports(no_lamports)
        nfts_avg, nfts_total, nfts_median, nfts_mode = nft_info(populated_df)
        lamports_avg, lamports_median, lamports_mode, sol_avg, sol_total = bal_info(
            populated_df
        )

        analytics_dict = {
            "community": [key],
            "date": [date],
            "users": [len(df)],
            "sol_avg": [sol_avg],
            "sol_total": [sol_total],
            # 'lamports_avg':[lamports_avg],
            # 'lamports_median':[lamports_median],
            # 'lamports_mode':[lamports_mode],
            "nfts_avg": [nfts_avg],
            "nfts_total": [nfts_total]
            # 'nfts_median':[nfts_median],
            # 'nfts_mode':[nfts_mode]
        }

        analytics_df = pd.DataFrame.from_dict(analytics_dict)
        analytics_df = analytics_df.set_index("community")
        result = [populated_df, analytics_df]
        results[key] = result

    return results


def grapescores(csvs):
    for key in list(csvs.keys()):
        df = csvs[key][1]
        users = df["users"].values[0]
        nftnum = df["nfts_total"].values[0]
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

        user_gscore = float(users) / float(holders)
        nft_gscore = float(nftnum) / float(supply)

        df["user_grape_score"] = str(round(user_gscore * 100, 2)) + "%"
        df["nft_grape_score"] = str(round(nft_gscore * 100, 2)) + "%"


def leaderboard(csvs):
    usernum = {}
    solavg = {}
    soltotal = {}
    nftsavg = {}
    nftstotal = {}
    nftgrapescore = {}
    usergrapescore = {}
    for key in list(csvs.keys()):
        df = csvs[key][1]
        name = df.index.values[0]
        users = df["users"].values[0]
        sol_avg = df["sol_avg"].values[0]
        sol_total = df["sol_total"].values[0]
        nfts_avg = df["nfts_avg"].values[0]
        nfts_total = df["nfts_total"].values[0]
        nft_grape_score = df["nft_grape_score"].values[0]
        user_grape_score = df["user_grape_score"].values[0]
        usernum[name] = users
        solavg[name] = sol_avg
        soltotal[name] = sol_total
        nftsavg[name] = nfts_avg
        nftstotal[name] = nfts_total
        nftgrapescore[name] = nft_grape_score
        usergrapescore[name] = user_grape_score

    userdf = pd.DataFrame(usernum, index=["Users"])
    solavgdf = pd.DataFrame(solavg, index=["Sol Average"])
    totsoldf = pd.DataFrame(soltotal, index=["Sol Total"])
    nftsavgdf = pd.DataFrame(nftsavg, index=["NFTs Average"])
    totnftsdf = pd.DataFrame(nftstotal, index=["NFTs Total"])
    nftgrapescoredf = pd.DataFrame(nftgrapescore, index=["NFT Grape Score"])
    usergrapescoredf = pd.DataFrame(usergrapescore, index=["User Grape Score"])

    return [
        userdf,
        solavgdf,
        totsoldf,
        nftsavgdf,
        totnftsdf,
        nftgrapescoredf,
        usergrapescoredf,
    ]


def leaderboard_save(csvs):
    for csv in csvs:
        filename = "../metrics/leaderboards/" + csv.index.values[0] + ".csv"
        csv.to_csv(filename)


# Replace names correspondingly
def run():
    paths = [
        "../csvs/smb.csv",
        "../csvs/aurory.csv",
        "../csvs/degens.csv",
        "../csvs/frakt.csv",
        "../csvs/gecko.csv",
        "../csvs/meerkat.csv",
        "../csvs/solsteads.csv",
        "../csvs/stylishstuds.csv",
        "../csvs/thugz.csv",
    ]
    csvs_preanalysis = csvdict(paths)
    csvs_postanalysis = analyze(csvs_preanalysis)
    grapescores(csvs_postanalysis)
    csvs_leaderboard = leaderboard(csvs_postanalysis)
    leaderboard_save(csvs_leaderboard)
    # revise csvsave
    # csvsave(csvs_leaderboard)
