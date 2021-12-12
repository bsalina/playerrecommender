import pandas as pd
import numpy as np 
from scipy.spatial import distance
from pyspark.sql import SparkSession
from sklearn.preprocessing import StandardScaler
# spark = SparkSession.builder.master("local[*]").appName('PySpark_Tutorial').getOrCreate()


def recommender(player):
    df = pd.read_csv('backend/players_20.csv')

    df1=df.iloc[:,0:20]
    df2=df.iloc[:,20:40]
    df3=df.iloc[:,40:60]
    df4=df.iloc[:,60:80]
    df5=df.iloc[:,80:]
    df1.describe().transpose()


    df1=df1.drop(['sofifa_id', 'player_url', 'long_name', 'age', 'dob',
        'height_cm', 'weight_kg', 'nationality', 'club', 'overall', 'potential',
        'value_eur', 'wage_eur','international_reputation','player_positions','preferred_foot'],axis=1)


    df2=df2.drop(['body_type', 'real_face', 'release_clause_eur', 'team_jersey_number', 'loaned_from', 'joined',
        'contract_valid_until', 'nation_jersey_number',"nation_position",'player_tags','team_position','gk_diving', 'gk_handling', 'gk_kicking'],axis=1)
    df2=df2.fillna(0)
    df3=df3.drop(["player_traits",'gk_reflexes', 'gk_speed', 'gk_positioning'],axis=1)

    df3=df3.fillna(0)

    df4=df4.drop(["ls","st"],axis=1)

    df=pd.concat([df1,df2,df3,df4],axis=1)

    df["weak_foot"].unique()

    def wr(x):
        x=x.split("/")
        return x[0]
    df["offensive_work_rate"]=df["work_rate"].apply(lambda x: wr(x))


    def wr(x):
        x=x.split("/")
        return x[1]
    df["defensive_work_rate"]=df["work_rate"].apply(lambda x: wr(x))


    df=df.drop(["work_rate"],axis=1)


    df["offensive_work_rate"].unique()

    def wr(x):
        if x=="High":
            return 0
        elif x=="Medium":
            return 1
        else:
            return 2
    df["offensive_work_rate"]=df["offensive_work_rate"].apply(lambda x: wr(x))

    def wr(x):
        if x=="High":
            return 0
        elif x=="Medium":
            return 1
        else:
            return 2
    df["defensive_work_rate"]=df["defensive_work_rate"].apply(lambda x: wr(x))

    X=df.drop(["short_name"],axis=1)


    
    if player:
        player_name=player
    p_ind=df[df["short_name"]==player_name].index[0]

    dist=[]
    for i in range (0,len(X.index)):
        dist.append(distance.euclidean(X.iloc[p_ind].values,X.iloc[i].values))

    pd.Series(dist)
    
    sn=df["short_name"].to_list()

    sim={"name":sn,"distance":dist}

    sim=pd.DataFrame(sim)

    sim.iloc[sim["distance"].sort_values().index]

    #from scipy import spatial
    #cossim=[]
    #for i in range (0,len(X.index)):
    #    cossim.append(1 - spatial.distance.cosine(X.iloc[p_ind].values,X.iloc[i].values))
    #pd.Series(cossim)
    #sim2={"name":sn,"cossim":cossim}
    #sim2=pd.DataFrame(sim2)
    #sim2.iloc[sim2["cossim"].sort_values(ascending=False).index]
    std=StandardScaler()

    X=std.fit_transform(X)

    #cossim=[]
    #for i in range (0,len(X)):
    #    cossim.append(1 - spatial.distance.cosine(X[p_ind],X[i]))
    #pd.Series(cossim)
    #sim2={"name":sn,"cossim":cossim}
    #sim2=pd.DataFrame(sim2)

    #sim2.iloc[sim2["cossim"].sort_values(ascending=False).index]

    dist=[]
    for i in range (0,len(X)):
        dist.append(distance.euclidean(X[p_ind],X[i]))
    pd.Series(dist)
    sim={"name":sn,"distance":dist}
    sim=pd.DataFrame(sim)
    print(sim.iloc[sim["distance"].sort_values().index])
    return (sim.iloc[sim["distance"].sort_values().index])

