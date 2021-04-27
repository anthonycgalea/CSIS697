from flask import Flask,jsonify,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'RateMyStudents.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False, unique=True)

  reviews = db.relationship('Review',backref='student',cascade='all,delete,delete-orphan',lazy=True) 

  def __repr__(self):
    return f'<Student(id={self.id}, name={self.name}, email={self.email})>'

  def to_dict(self):
    d={}
    d['avg_rating']=self.gen_avg_rating()
    d['email']=self.email
    d['name']=self.name

    reviews_dict = [review.to_dict() for review in self.reviews]
    if len(reviews_dict) > 0:
      d['reviews'] = reviews_dict
    else:
      d['reviews'] = f"Bummer, {self.name} does not have any reviews yet. Check back later."
    return d

  def overview(self):
    d={}
    d['avg_rating']=self.gen_avg_rating()
    d['email']=self.email
    d['name']=self.name
    return d

  def gen_avg_rating(self): #fix this anthony
      sum=0
      cnt=0
      for review in self.reviews:
        sum+=review.get_overall_score()
        cnt+=1
      if (cnt != 0):
        return sum/cnt
      else:
        return "N/A"

class Review (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    course=db.Column(db.String(100),nullable=False)
    author=db.Column(db.String(100), default='Anonymous')
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    review=db.Column(db.String(1000), default='This student is the worst student I have seen in all my life.')
    intelligence=db.Column(db.Integer, db.CheckConstraint('intelligence>=1 and intelligence <=5'),  default=3)
    attendance=db.Column(db.Integer,db.CheckConstraint('attendance>=1 and attendance <=5'),  default=3)
    participation=db.Column(db.Integer,db.CheckConstraint('participation>=1 and participation <=5'),  default=3)
    sarcasm=db.Column(db.Integer, db.CheckConstraint('sarcasm>=1 and sarcasm <=5'), default=3)

    def __repr__(self):
        return f'<Review(id={self.id}, course={self.course}, author={self.author}, student_id={self.student_id}, review={self.review}, intelligence={self.intelligence}, attendance={self.attendance}, participation={self.participation}, sarcasm={self.sarcasm})>'

    def to_dict(self):
        d={}
        d['attendance']=self.attendance
        d['author']=self.author
        d['course']=self.course
        d['intelligence']=self.intelligence
        d['overall_score']=self.get_overall_score()
        d['participation']=self.participation
        d['review']=self.review
        d['sarcasm']=self.sarcasm
        return d

    def get_overall_score(self):
        return (self.intelligence+self.attendance+self.participation+self.sarcasm)/4
    


def init_db():

    db.create_all()
    db.session.add(Student(name="Harry Potter",email="hpotter@hogwarts.edu"))
    db.session.add(Student(name="Hermione Granger",email="granger@hogwarts.edu"))
    db.session.add(Student(name="Viktor Krum",email="krum@durmstrang.edu"))
    db.session.add(Student(name="Tom Marvolo Riddle",email="iamlordvoldemort@hogwarts.edu"))
    db.session.add(Student(name="Ron Weasley",email="ronny@hogwarts.edu"))
    db.session.add(Student(name="Fleur Delacour",email="fleur@beauxbatons.edu"))
    
    db.session.add(Review(course="Potions-102",student_id=1,review="Mr. Potter is the most arrogant student to have stepped foot into my classroom! ", intelligence=1,attendance=1,sarcasm=5,participation=1))
    db.session.add(Review(course="Charms-401",student_id=1,review="Harry is a brilliant student. He is well on his way to becoming a world famous Auror. ",author='Prof. Flitwick', intelligence=5,attendance=5,sarcasm=5,participation=5))
    db.session.add(Review(course="Herbology-116",student_id=1,review="Potter is one of the smartest students, I have known. He would ace this class, if he didn't sneak out of his dorm every night.  ", intelligence=4,attendance=1,participation=5))
    db.session.add(Review(course="Potions-102",student_id=2,review="Ms. Grainger has the unique distinction of being an insufferable know-it-all ", intelligence=5,attendance=5,participation=1,sarcasm=1))
    db.session.add(Review(course="DADA-400",student_id=2,review="Best student ever!", intelligence=5,attendance=5,participation=5,sarcasm=5))
    db.session.add(Review(course="Quidditch-101",student_id=3,intelligence=1,attendance=5,review="Future World cup Winner!"))
    db.session.add(Review(course="Transfiguration-301",student_id=4,intelligence=5,attendance=5,participation=1,review="A brilliant student. But seems a bit odd. He seems fixated on creating Horcruxes."))
    db.session.add(Review(course="Charms-401",student_id=5,review="Another Weasley! Atleast this one's not as much of a troublemaker like his brothers."))
    db.session.commit()

#init_db()
@app.route('/')
def index():
    return render_template('index.html',bg_file='blog_bg.jpg')



@app.route('/students')
def viewAllStudents():
    res = Student.query.all()
    dlist=[r.overview() for r in res]
    print(dlist)
    return jsonify(dlist)

@app.route('/student',methods=['POST'])
def createStudent():
    temp = Student(**request.json)
    db.session.add(temp)
    db.session.commit()
    return jsonify(temp.overview())


@app.route('/reviews/<studentEmail>')
def viewStudentReviews(studentEmail):
    res = Student.query.filter_by(email = studentEmail ).first_or_404()
    d = res.to_dict()
    return jsonify(d)

@app.route('/students/<studentEmail>',methods=['DELETE'])
def deleteStudent(studentEmail):
    res = Student.query.filter_by(email = studentEmail ).first_or_404()
    db.session.delete(res)
    db.session.commit()
    return jsonify({'message' : 'Student Deleted.'})

@app.route('/reviews/<studentEmail>',methods=['POST'])
def createReview(studentEmail):
    res = Student.query.filter_by(email = studentEmail ).first_or_404()
    temp = Review(**request.json)
    temp.student_id=res.id
    db.session.add(temp)
    db.session.commit()
    return jsonify({'message' : 'Review Posted.'})

@app.route('/reviews/<int:reviewId>',methods=['DELETE'])
def deleteReview(reviewId):
    res = Review.query.filter_by(id = reviewId ).first_or_404()
    db.session.delete(res)
    db.session.commit()
    return jsonify({'message' : 'Review Deleted.'})


if __name__ == '__main__':
    app.run(debug=True)

