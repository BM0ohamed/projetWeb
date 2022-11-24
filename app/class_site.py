# -*- coding: utf-8 -*-

#faut débugger le nom des pays et créer de meilleurs structures
#de données là

from ast import Try
import random
import sqlite3
import urllib.request
from PIL import Image
import webbrowser
from bdd_comm import *
# from geopy.geocoders import Nominatim
# import pycountry_convert as pc


# def country_to_continent(country_name):
#     if country_name == "Kosovo": #il reconnait pas le kosovo ce golmon
#         return "Europe"
#     else:
#         try:
#             country_alpha2=pc.country_name_to_country_alpha2(country_name)
#             country_continent_code=pc.country_alpha2_to_continent_code(country_alpha2)
#             country_continent_name=pc.convert_continent_code_to_continent_name(country_continent_code)
#             return country_continent_name
#         except KeyError:
#             return "Unknown"
class bdd_sites:
    def __init__(self,nom_du_fichier):
        self.__conn = sqlite3.connect(nom_du_fichier)
        
    
    # def ajouter_pays_continent(self):#Cette methode ne doit pas etre appellée
    #     #elle ajoute les pays et continents dans la bdd mais faut pas y toucher
    #     curseur=self.__conn.cursor() 
    #     curseur.execute("select name from sites")
    #     liste= curseur.fetchall()
    #     for k in range(len(liste)):
    #         p=self.pays(liste[k][0])
    #         c=self.continent(liste[k][0])
    #         curseur.execute("update sites set pays='{}', continent='{}' where name='{}'".format(p,c,liste[k][0]))
    #         self.__conn.commit()

    def liste_lieux(self,continent=None):#pas ouf ce code très long et pas opti
        if continent==None: 
            curseur=self.__conn.cursor() 
            curseur.execute("SELECT name from sites")
            liste= curseur.fetchall()
            liste_f=[]
            for k in range(len(liste)):
                liste_f.append(liste[k][0])
            return liste_f
        else:
            curseur=self.__conn.cursor() 
            curseur.execute("SELECT name from sites where continent='{}'".format(continent))
            liste= curseur.fetchall()
            liste_f=[]
            for k in range(len(liste)):
                liste_f.append(liste[k][0])
            return liste_f

    def nombre_lieux(self):
        curseur=self.__conn.cursor() 
        curseur.execute("select count(*) from sites")
        return curseur.fetchone()[0]
    
    def coord(self,lieu): #renvoie le tuple (latitude,longitude)
        curseur=self.__conn.cursor() 
        curseur.execute("select lat, lon from sites where name='{}'".format(lieu))
        return curseur.fetchone()
    
    def liste_coord(self):
        curseur=self.__conn.cursor() 
        curseur.execute("select lat, lon from sites")
        liste= curseur.fetchall()
        return liste
    
    def photo(self,lieu):
        curseur=self.__conn.cursor() 
        curseur.execute("select photo from sites where name='{}'".format(lieu))
        lien= curseur.fetchone()[0]
        # print(urllib.request.urlretrieve(lien,"gfg.png"))
        return lien
        
    def description(self,lieu):
        curseur=self.__conn.cursor() 
        curseur.execute("select abstract from sites where name='{}'".format(lieu))
        return curseur.fetchone()[0]
    def wiki(self,lieu):
        curseur=self.__conn.cursor() 
        curseur.execute("select wiki from sites where name='{}'".format(lieu))
        lien= curseur.fetchone()[0]
        #webbrowser.open(lien)
        return(lien)
   
    # def pays(self,lieu): #retourne le pays d'un site donné
    #     geolocator = Nominatim(user_agent="geoapiExercises")
    #     c=self.coord(lieu)
    #     location = geolocator.reverse(str(c[0])+","+str(c[1]),language='en')
    #     if location == None:
    #         return "pays inconnu"
    #     address = location.raw['address']
    #     country = address.get('country', '')
    #     return country

    def continent2(self,lieu):
        cursuer=self.__conn.cursor()
        cursuer.execute("select continent from sites where name='{}'".format(lieu))
        return cursuer.fetchone()[0]

    # def continent(self,lieu):
    #     p=self.pays(lieu)
    #     if p=="pays inconnu":
    #         return "Probablement Oceanique"
    #     return country_to_continent(p)
    
    def pays2(self,lieu):
        curseur=self.__conn.cursor()
        curseur.execute("select pays from sites where name='{}'".format(lieu))
        return curseur.fetchone()[0]

    def findLieu(self,coord):
        curseur=self.__conn.cursor()
        curseur.execute("select name from sites where lat={} and lon={}".format(coord[0],coord[1]))
        return curseur.fetchone()[0]

    def information(self,lieu):
        ObjetComm =Comment('bdd_commentaire.db')
        res={
            "nom": lieu,
            "continent": self.continent2(lieu),
            "pays": self.pays2(lieu),
            "coord": self.coord(lieu),
            "description": self.description(lieu),
            "wiki": self.wiki(lieu),
            "photo": self.photo(lieu),
            "comments": ObjetComm.site_comment(lieu)
            # "image": self.photo(lieu)
        }
        # res["continent"]=self.continent(lieu)
        # res["pays"]=self.pays(lieu)
        # res["coord"]=self.coord(lieu)
        # res["description"]=self.description(lieu)
        # res["wiki"]=self.wiki(lieu)
        # res["image"]=self.photo(lieu)
        return res
    
    # def information_coord(self,coord):
    #     lieu=self.findLieu(coord)
    #     ObjetComm =Comment('bdd_commentaire.db')
    #     res={
    #         "nom": lieu,
    #         "continent": self.continent(lieu),
    #         "pays": self.pays(lieu),
    #         "coord": self.coord(lieu),
    #         "description": self.description(lieu),
    #         "wiki": self.wiki(lieu),
    #         "photo": self.photo(lieu),
    #         "comments": ObjetComm.site_comment(lieu)
    #         # "image": self.photo(lieu)
    #     }
    #     # res["continent"]=self.continent(lieu)
    #     # res["pays"]=self.pays(lieu)
    #     # res["coord"]=self.coord(lieu)
    #     # res["description"]=self.description(lieu)
    #     # res["wiki"]=self.wiki(lieu)
    #     # res["image"]=self.photo(lieu)
    #     return res
    
    def send_three_random_sites(self):
        liste=self.liste_lieux()
        n1, n2, n3 = random.sample(range(0, len(liste) - 1), 3)
        return [self.information(liste[n1]), self.information(liste[n2]), self.information(liste[n3])]

    def __str__(self,lieu):
        a = "Continent : "+ self.continent2(lieu)+"\n" + "Pays : "+self.pays2(lieu) + "\n" + "Coordonnées : " + str(self.coord(lieu))
        print(a)
        print(self.description(lieu))
        self.photo(lieu)
        print("\n le lien wiki est : "+self.wiki(lieu))

# if __name__== '__main__':
#     sites =bdd_sites("sites.db")
#     print(sites.information("Vieux Lyon"))
#     print(sites.information_coord((14.916, -23.606)))