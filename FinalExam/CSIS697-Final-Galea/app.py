from flask import Flask,jsonify,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'Ecommerce.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  user_name = db.Column(db.String(50), nullable=False, unique=True)
  balance = db.Column(db.Integer, default=100)

  items = db.relationship('Item',backref='user',cascade='all,delete,delete-orphan',lazy=True) 

  def __repr__(self):
    return f'<User(id={self.id}, name={self.name}, user_name={self.user_name}, balance={self.balance})>'

  def to_dict(self):
    d={}
    d['balance']=self.balance
    items_dict = [item.to_dict() for item in self.items]
    if len(items_dict) > 0:
      d['items'] = items_dict
    else:
      d['items'] = f"{self.user_name} does not have any items for sale at the moment. Check back later."

    d['name']=self.name
    d['user_name']=self.user_name

    return d


class Item (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    

    def __repr__(self):
        return f'<Review(id={self.id}, course={self.course}, author={self.author}, student_id={self.student_id}, review={self.review}, intelligence={self.intelligence}, attendance={self.attendance}, participation={self.participation}, sarcasm={self.sarcasm})>'

    def to_dict(self):
        d={}
        d['id']=self.id
        d['name']=self.name
        d['owner']=self.owner
        d['price']=self.price
        return d

       


def init_db():
    db.create_all()
    u1 = User(name="Chris Evans",user_name="steve123")
    db.session.add(u1)
    db.session.add(User(name="Paul Bettany",user_name="thevision"))
    db.session.add(User(name="Paul Rudd",user_name="antpaul"))
    db.session.add(User(name="Robert Downey Jr.",user_name="iamironman"))
    db.session.add(User(name="Chris Hemsworth",user_name="noobmaster69"))
    
    db.session.add(Item(name="Vibranium Shield. (Lightly used.)",owner=1,price=55))
    db.session.add(Item(name="Mjolnir - The Hammer of the Gods",owner=5,price=95))
    db.session.add(Item(name="Jarvis - A sophisticated AI",owner=4,price=120))
    db.session.add(Item(name="Mark XLIV - Hulkbuster",owner=4,price=80))
    db.session.add(Item(name="Mindstone - The rarest stone on earth",owner=2,price=90))
   
    db.session.commit()

#init_db()
@app.route('/')
def index():
    return render_template('index.html',bg_file='blog_bg.jpg')



@app.route('/user')
def viewAllUsers():
    res = User.query.all()
    dlist=[r.to_dict() for r in res]
    print(dlist)
    return jsonify(dlist)

@app.route('/user/<user_name>')
def viewSellerInfo(user_name):
    res = User.query.filter_by(user_name = user_name).first_or_404()
    d = res.to_dict()
    return jsonify(d)

@app.route('/user',methods=['POST'])
def createUser():
    temp = User(**request.json)
    failed=False
    try:
        db.session.add(temp)
        db.session.commit()
    except:
        failed=True
        db.session.rollback()
        db.session.flush() # this resets the add transaction
    if failed:
        return jsonify({"error":"User could not be created."}), 400 #send back a status code of 400
    else:
        # complete this part. Return a json representation of the user similar to /get
        return jsonify(temp.to_dict())


@app.route('/item')
def viewAllItems():
    res = Item.query.all()
    dlist=[r.to_dict() for r in res]
    print(dlist)
    return jsonify(dlist)

@app.route('/item/<int:itemId>')
def viewItemInfo(itemId):
    res = Item.query.filter_by(id = itemId).first_or_404()
    d = res.to_dict()
    return jsonify(d)

@app.route('/students/<studentEmail>',methods=['DELETE'])
def deleteStudent(studentEmail):
    res = Student.query.filter_by(email = studentEmail ).first_or_404()
    db.session.delete(res)
    db.session.commit()
    return jsonify({'message' : 'Student Deleted.'})

@app.route('/item/sell',methods=['POST'])
def sellItem():
    temp = Item(**request.json)
    failed=False
    try:
        db.session.add(temp)
        db.session.commit()
    except:
        failed=True
        db.session.rollback()
        db.session.flush() # this resets the add transaction
    if failed:
        return jsonify({"error":"Item could not be created."}), 400 #send back a status code of 400
    else:
        # complete this part. Return a json representation of the user similar to /get
        return jsonify(temp.to_dict())

@app.route('/item/buy',methods=['PUT'])
def buyItem():
    resItem = Item.query.filter_by(id = request.get_json()['item_id'] ).first_or_404()
    resUser = User.query.filter_by(user_name = request.get_json()['user_name']).first_or_404()
    resOwner = User.query.filter_by(id = resItem.owner ).first_or_404()
    if resItem.owner==resUser.id:
      return jsonify({'message' : 'You cannot buy your own items.'})
    elif resItem.price > resUser.balance:
      return jsonify({'message' : 'You cannot afford this item.'})
    else:
      resItem.owner=resUser.id
      resOwner.balance+=resItem.price
      resUser.balance-=resItem.price
      db.session.commit()
      return jsonify({'message' : f'Thanks {resUser.user_name} for buying {resItem.name}.'})


if __name__ == '__main__':
    app.run(debug=True)

