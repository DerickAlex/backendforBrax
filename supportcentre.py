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


class supportcentre(db.Model):
    __table__name = 'supportcentre'
    projectID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    subjects = db.Column(db.String(50))
    Issue = db.Column(db.String(50))



@app.route('/supportcentre', methods=['POST'])
@cross_origin()
def submit():
    data = request.get_json(force=True)

    new_appeal = supportcentre(projectID=data['projectid'], email=data['email'], subjects=data['subjects'],
                               Issue=data['issue'])
    db.session.add(new_appeal)
    db.session.commit()

    return jsonify({'message': 'Your Appeal has been submitted'})



@app.route('/supportcentre/getallappeals', methods=['GET'])
def get_all_appeals():
    appeals = supportcentre.query.all()
    output = []
    for appeal in appeals:
        appeal_data = {}
        appeal_data['projectID'] = appeal.projectID
        appeal_data['email'] = appeal.email
        appeal_data['subjects'] = appeal.subjects
        appeal_data['Issue'] = appeal.Issue
        output.append(appeal_data)

    return jsonify({'appeals': output})



