from flask import Flask, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_cors import CORS, cross_origin


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

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    admin = db.Column(db.Boolean)
    user_type = db.Column(db.String(20))
    phone_number = db.Column(db.String(20))


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['email'] = user.email
        user_data['admin'] = user.admin
        user_data['user_type'] = user.user_type
        user_data['phone_number'] = user.phone_number
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['email'] = user.email
    user_data['admin'] = user.admin
    user_data['user_type'] = user.user_type
    user_data['phone_number'] = user.phone_number

    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
@cross_origin()
def create_user():
    data = request.get_json(force=True)

    hashed_password = generate_password_hash(data['password'], method='sha256', salt_length=8)

    new_user = User(public_id=str(uuid.uuid4()), username=data['full_name'], password=hashed_password,
                    email=data['email'], user_type=data['user_type'], phone_number=data['phone'], admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': "The User has been promoted"})


@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


# Login Part

@login_manager.user_loader
def load_user(public_id):
    return User.query.get(int(public_id))


@app.route('/login', methods=['POST'])
def login():
    # email = request.headers.get('email')
    # password = request.headers.get('password')

    data = request.get_json(force=True)

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'logged in!'})

    return jsonify({'message': 'invalid login details' })


if __name__ == '__main__':
    app.run(debug=True)
