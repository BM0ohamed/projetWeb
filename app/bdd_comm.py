from datetime import datetime
import sqlite3

class Comment: #classe de liste de commentaire pour un lieu donné 

    def __init__(self,nom_bdd): 
        self.__conn = sqlite3.connect(nom_bdd)

    
    def ajout_comment(self,data):
        cur=self.__conn.cursor()
        now = datetime.now()
        date=now.strftime("%d/%m/%Y")
        heure=now.strftime("%H:%M")
        sql='insert into commentaire (user, site, date, heure, contenu) values (?, ?, ?, ?, ?)'
        value=(data["user"],data["site"],date,heure,data["contenu"])
        cur.execute(sql,value)
        self.__conn.commit()
        
    
    def site_comment(self,lieu): #on prend 3 commentaires max sur un site 
        cur=self.__conn.cursor()
        cur.execute("select * from commentaire where site='{}' order by date desc, heure desc limit 3".format(lieu))
        liste=cur.fetchall()
        a=[] #la liste des dictionnaires
        for i in range(len(liste)):
            b=liste[i]
            dico={"user" : b[0],"date" : b[2],"heure" : b[-1],"contenu" : b[3]}
            a.append(dico)
        return a

# if __name__=='__main__':
#     test=Comment('bdd_commentaire.db')
#     print(test.site_comment("Vieux Lyon"))
