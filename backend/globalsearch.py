import pandas as pd


def search(position,ageTo,ageFrom,strongFoot,potential,reputation,price):
    originalData = pd.read_csv('backend/players_20.csv')
    if position:
        originalData = originalData[originalData['player_positions'].str.lower().str.contains(position)]
    if ageTo:
        originalData= originalData.query('age<='+str(ageTo))
    if ageFrom:
        originalData= originalData.query('age>='+str(ageFrom))
    if strongFoot:
        originalData= originalData[ originalData['preferred_foot'].str.lower().str.contains(strongFoot)]
    if potential:
        originalData= originalData.query('potential>='+str(potential))
    if reputation:
        originalData= originalData.query('international_reputation>='+str(reputation))
    if price:
        originalData= originalData[originalData['value_eur'].astype(int)<int(price)]
    return originalData

def searchById(playerId):
    allData= pd.read_csv('backend/players_20.csv')
    currentPlayer=allData[["sofifa_id","short_name","long_name","age","nationality","potential","international_reputation","player_positions","value_eur","preferred_foot","club"]].query(('sofifa_id==')+str(playerId))
    return currentPlayer



