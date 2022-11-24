from flask import Flask, render_template, jsonify, request, redirect
from class_site import *
import random
import time
from bdd_comm import *
app = Flask(__name__)

@app.route('/')
def index():
    ObjetSite=bdd_sites("sites.db")
    liste=ObjetSite.liste_lieux()
    liste_cord=ObjetSite.liste_coord()
    markers=[]
    site=request.args.get("site")

    if site != None:
        print(site)
        return jsonify(ObjetSite.information(site))
    else:
        for i in range(len(liste)):
            lieu=liste[i]
            cord=liste_cord[i]
            markers+=[
                {
                'lat':cord[0],
                'lon':cord[1],
                'popup':lieu
                }
            ]
        return render_template('index.html',markers = markers )


@app.route('/accueil')
def accueil():
    ObjetSite=bdd_sites("sites.db")
    liste=ObjetSite.liste_lieux()
    liste_cord=ObjetSite.liste_coord()
    markers=[]
    site=request.args.get("site")

    if site != None:
        print(site)
        return jsonify(ObjetSite.information(site))
    else:
        for i in range(len(liste)):
            lieu=liste[i]
            cord=liste_cord[i]
            markers+=[
                {
                'lat':cord[0],
                'lon':cord[1],
                'popup':lieu
                }
            ]
        return render_template('index.html',markers = markers )

@app.route('/restedum.html')
def reste():
    site=request.args.get("site")
    ObjetSite=bdd_sites("sites.db")
    if site != None:
        return jsonify(ObjetSite.information(site))
    else:
        liste1=ObjetSite.liste_lieux("Oceania")
        return render_template('restedum.html', sites_historiques=liste1)

@app.route('/amerique')
def amerique():
    site=request.args.get("site")
    ObjetSite=bdd_sites("sites.db")
    if site != None:
        return jsonify(ObjetSite.information(site))
    else:
        liste1=ObjetSite.liste_lieux("North America")
        liste2=ObjetSite.liste_lieux("South America")
        liste=liste1+liste2
        return render_template('amerique.html', sites_historiques=liste)

@app.route('/afrique')
def afrique():
    site=request.args.get("site")
    ObjetSite=bdd_sites("sites.db")
    if site != None:
        return jsonify(ObjetSite.information(site))
    else:
        liste=ObjetSite.liste_lieux("Africa")
        return render_template('afrique.html', sites_historiques=liste)

@app.route('/europe', methods=['GET'])
def europe():
    site=request.args.get("site")
    ObjetSite=bdd_sites("sites.db")

    if site != None:
        return jsonify(ObjetSite.information(site))
    else:
        liste=ObjetSite.liste_lieux("Europe")
        return render_template('europe.html', sites_historiques=liste)

@app.route('/asie')
def asie():
    site=request.args.get("site")
    ObjetSite=bdd_sites("sites.db")

    if site != None:
        return jsonify(ObjetSite.information(site))
    else:
        liste=ObjetSite.liste_lieux("Asia")
        return render_template('asie.html', sites_historiques=liste)

# On met le choix du site et de la liste hors de la route comme ça c'est toujours la même en fon
def reloadQuiz():
    global bon_site
    global bon_coord
    global liste_alea_quizz
    t1=time.time_ns()
    ObjetSite=bdd_sites("sites.db")
    liste_alea_quizz=ObjetSite.send_three_random_sites()
    n = random.randint(0,2)
    bon_site=liste_alea_quizz[n]["nom"]
    bon_coord=liste_alea_quizz[n]["coord"]

reloadQuiz()
@app.route('/quiz', methods=['POST','GET'])
def quiz():    
    t1=time.time_ns()

    # Est-ce que l'utilisateur envoie un guess et est-ce qu'il est bon
    if request.method == 'POST':
        guess = request.json["siteSelected"]
        if guess != None:
            isGoodSite = bon_site == guess
            goodSiteIs = bon_site
            
            reloadQuiz()
            return jsonify({"isGoodSite": isGoodSite, "goodSiteIs": goodSiteIs})     
        else:
            return jsonify({"isGoodSite": False, "erreur": "no value : {}".format(guess)})
    #on formatte les coordonnées pour les envoyer à la carte
    coordFormatted = {
        'lat': bon_coord[0],
        'lon': bon_coord[1]
    }
    return render_template('quiz.html', sites=liste_alea_quizz, coord=coordFormatted)

@app.route('/europe', methods=['GET','POST'])
def manage_comment():
    if request.method == "POST":
        global pseudo
        global contenu
        global lieu 
        pseudo = request.form.get("pseudo")
        contenu= request.form.get("contenu_commentaire")
        if not pseudo :
            return ''' <h1>Veuillez renseigner un pseudo</h1> '''
        if not contenu :
            return ''' <h1>Votre commentaire est vide</h1> '''
        lieu = request.form.get("lieu")
    return redirect(request.referrer) 



if __name__ == '__main__':
    port=8082
    app.run(host="localhost", port=port, debug=True)
