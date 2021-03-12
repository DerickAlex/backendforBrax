from flask import Flask, request, jsonify, flash
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///braxDB.db'

db = SQLAlchemy(app)


class NewProject(db.Model):
    __table__name = 'NewProject'
    projectName = db.Column(db.String, unique=True)
    projectDescription = db.Column(db.String(50), unique=True)
    projectDate = db.Column(db.String(50))


@app.route('/newproject', methods=['POST'])
@cross_origin()
def submit():
    data = request.get_json(force=True)

    new_project = NewProject(projectName=data['****'], projectDescription=data['***'], subjects=data['****'])
    db.session.add(new_project)
    db.session.commit()

    return jsonify({'message': 'Your New Project has been added'})