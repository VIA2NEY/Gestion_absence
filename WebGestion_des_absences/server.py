from flask import Flask, render_template , jsonify, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__ , static_url_path='/static')



app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/pfe_gabsiit"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# Définition des classes correspondant aux tables

class Utilisateurs(db.Model):
    ID_Utilisateur = db.Column(db.Integer, primary_key=True)
    loginname = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    Type = db.Column(db.String(255), nullable=False)

class Departement(db.Model):
    Id_dep = db.Column(db.Integer, primary_key=True)
    specialiter = db.Column(db.String(255), nullable=False)
    niveau = db.Column(db.String(255), nullable=False)

class Etudiant(db.Model):
    ID_Utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.ID_Utilisateur'), primary_key=True)
    Id_departement = db.Column(db.Integer, db.ForeignKey('departement.Id_dep'), nullable=False)
    matricule = db.Column(db.Integer, nullable=False)
    nom = db.Column(db.String(55), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(55), nullable=False)
    Date_De_Nainssance = db.Column(db.Date, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.LargeBinary)

class Admin(db.Model):
    ID_Utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.ID_Utilisateur'), primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)

class Enseignants(db.Model):
    ID_Utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.ID_Utilisateur'), primary_key=True)
    Nom = db.Column(db.String(255), nullable=False)
    Prenom = db.Column(db.String(255), nullable=False)
    Tel = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    Photo = db.Column(db.LargeBinary)

class Presence(db.Model):
    ID_Presence = db.Column(db.Integer, primary_key=True)
    ID_Etudiant = db.Column(db.Integer, db.ForeignKey('etudiant.ID_Utilisateur'), nullable=False)
    ID_Cour = db.Column(db.Integer, db.ForeignKey('cour.idCour'), nullable=False)
    dateheure = db.Column(db.DateTime, nullable=False)
    Statut = db.Column(db.String(255), nullable=False)

class Cour(db.Model):
    idCour = db.Column(db.Integer, primary_key=True)
    dateheure = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    ID_Module = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NomModule = db.Column(db.String(255), nullable=False)
    nombre_Heur_du_modulee = db.Column(db.Integer, nullable=False)

class CodeQR(db.Model):
    ID_CodeQR = db.Column(db.Integer, primary_key=True)
    ID_Cour = db.Column(db.Integer, db.ForeignKey('cour.idCour'), nullable=False)
    Code = db.Column(db.String(255), nullable=False)


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == "POST":
        # recupere les info Json entrer dans le body qui sont de forme {"nom_user":"...","password":"..."}
        username = request.form.get("nom_user")
        password = request.form.get("Mdp")
        
        # crée variable utilisateur qui stocke les elements de la classe Utilisateurs recherche par nom cnx = loginname=nom_utilisateur (le nom dans la bd correspond au nom dans le body)
        utilisateur = Utilisateurs.query.filter_by(loginname=username).first()

        # si la propriete utilisateur est crée :
        if utilisateur:
            if utilisateur.password == password:
                role = utilisateur.Type
                response = jsonify({"message": "Authentification réussie"})
                response.status_code = 200
                # return render_template('vueindex_part_typeuser.html', Type=role)

                if utilisateur.Type == 'admin':
                    # session['utilisateurs'] = Utilisateurs.query.all()
                    # session['etudiants'] = Etudiant.query.all()
                    # session['enseignants'] = Enseignants.query.all()
                    # Autres données...

                    return redirect('/administrateur')
                elif utilisateur.Type == 'enseignant':
                    # session['module_affecte'] = EnseignantModule.query.filter_by(enseignant_id=current_user.id).first()
                    # session['absences'] = Absence.query.filter_by(module_id=session['module_affecte'].module_id).all()
                    # session['absences'] = Presence.query.filter_by(module_id=session['module_affecte'].module_id).all()
                    # Autres données...Presence

                    return redirect('/enseignant')
                
                elif utilisateur.Type == 'etudiant':
                    # session['etudiant'] = Etudiant.query.filter_by(id_etudiant=utilisateur.id).first()
                    
                    return redirect('/etudiant')
                
            
            else:
                response = jsonify({"message": "Mot de passe incorrect"})
                response.status_code = 401
                return response
        else:
            response = jsonify({"message": "Nom d'utilisateur incorrect"})
            response.status_code = 401

            return render_template('login.html', error_message=response)
    else:

        return render_template('login.html')


@app.route('/administrateur')
def indexpageadmin() :
    user = Utilisateurs.query.all()
    student = Etudiant.query.all()
    module =  Enseignants.query.all()

    return render_template('admin_index.html', utilisateurs=user, etudiants=student, enseignants=module)

@app.route('/enseignant')
def indexpageens() :

    attendancelist = Presence.query.all()

    return render_template('enseignant_index.html', listpresence=attendancelist)

@app.route('/etudiant')
def indexpageetd() :

    return render_template('etudiant_index.html',)

# ToDo oublie pas de verifier les redirect du chat s'il ramene vraiment les data dans la page 

@app.route('/a')
def testa():

    # return render_template('login.html')
    return render_template('TbListEnseignant.html')
@app.route('/b')
def testb():

    return render_template('TbListModule.html')

@app.route('/creation')
def testc():

    return render_template('creationEns_vue.html')

@app.route('/etd')
def testEtd():

    return render_template('creationEtd_vue.html')

@app.route('/mod')
def testMod():

    return render_template('creationModule_vue.html')

@app.route('/cmod')
def testChoixMod():

    return render_template('affectationMdl_vue.html')


# @app.route('/index/<role>',methods=['POST'])
# def auth(role)


# @app.route('/authentification',methods=['POST'])
# def auth():
    
    # username = request.form['nom_user']
    # password = request.form['Mdp']

    # if username == 'vianney' and password == '123' :
    
    #     return render_template('admin_index.html')

    # error_message = 'Identifiants incorrects. Veuillez réessayer.'
    # return render_template('login.html', error_message=error_message)

# Tester pour voir la liste des user
@app.route("/listuser", methods=['GET'])
def get_utilisateurs():
    utilisateurs = Utilisateurs.query.all()
    result = []
    for chaqueutilisateur in utilisateurs:
        utilisateur_datajson = {}
        utilisateur_datajson['ID_User'] = chaqueutilisateur.ID_Utilisateur
        utilisateur_datajson['Nom_user'] = chaqueutilisateur.loginname
        utilisateur_datajson['Mdp'] = chaqueutilisateur.password
        utilisateur_datajson['role_user'] = chaqueutilisateur.Type
        result.append(utilisateur_datajson)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)