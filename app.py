from flask import Flask, render_template, request
app = Flask(__name__)
from backend.recommendation import recommender
from backend.globalsearch import search,searchById

@app.route("/",methods=['GET'])
def index():
    return render_template('homepage.html')
@app.route("/",methods=["POST"])
def post_handler():
    print(request.form);
    position=request.form.get('position', "")
    ageTo= request.form.get('ageto', "")
    ageFrom=request.form.get('agefrom', "")
    dominantFoot= request.form.get('preferedfoot', "")
    rating = request.form.get('rating', "")
    potential= request.form.get('potential', "")
    price=request.form.get('price', "")
    players= search(position,ageTo,ageFrom,dominantFoot,potential,rating,price)
    print(players)
    players=players[["sofifa_id","short_name","long_name","age","nationality","potential","international_reputation","player_positions","value_eur","preferred_foot","club"]]
    #return render_template('homepage.html',tables=[players.to_html(classes='data')], titles=players.columns.values)
    return render_template("homepage.html", column_names=players.columns.values, row_data=list(players.values.tolist()),link_column="sofifa_id", zip=zip)

@app.route("/player",methods=['GET'])
def playerSearch():
    user = request.args.get('id')
    players=searchById(user)
    print(players['short_name'].values[0])
    similarPlayers=recommender(players['short_name'].values[0])
    return render_template('index.html',currentPlayers=[players.to_html(classes='data')], currentTitles=players.columns.values,simPlayers=[similarPlayers.to_html(classes='data')])
if __name__ == "__main__":
    app.run()