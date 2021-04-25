from flask import Flask,jsonify,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'student.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  gpa = db.Column(db.Float, db.CheckConstraint('gpa>=0 and gpa <=4'),nullable=False)

  blogs = db.relationship('Blog',backref='student',cascade='all,delete,delete-orphan',lazy=True) 

  def __repr__(self):
    return f'<Student(id={self.id}, name={self.name}, gpa={self.gpa})>'

  def to_dict(self):
    d={}
    d['id']=self.id
    d['name']=self.name
    d['gpa']=self.gpa
    
    blogs_dict = [b.overview() for b in self.blogs]
    d['blogs'] = blogs_dict
    return d

class Blog (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    content=db.Column(db.String(1000), default='Generic Blog Post')
    author = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)

    def __repr__(self):
        return f'<Blog(id={self.id}, title={self.content}, content={self.content},author={self.author})>'

    def to_dict(self):
        d={}
        d['id']=self.id
        d['title']=self.title
        d['content']=self.content
        d['author']=self.author
        return d

    def overview(self):
        d={}
        d['id']=self.id
        d['title']=self.title
        return d


def init_db():

    db.create_all()
    s1 = Student(name="Charlie",gpa=3.4)
    db.session.add(s1)
    db.session.add(Student(name="Josh",gpa=3.5))
    db.session.add(Student(name="Mary",gpa=3.25))
    db.session.add(Student(name="Peter",gpa=3.75))
    db.session.add(Student(name="Jack",gpa=3.0))
    
    db.session.add(Blog(title="Blog 1",author=1))
    db.session.add(Blog(title="Blog 2",author=1))
    db.session.add(Blog(title="Blog 3",author=1))
    db.session.add(Blog(title="Blog 4",author=2))
    db.session.commit()

#init_db()
@app.route('/')
def index():
    return render_template('index.html',bg_file='blog_bg.jpg')



@app.route('/students')
def viewAllStudents():
    res = Student.query.all()
    dlist=[r.to_dict() for r in res]
    print(dlist)
    return jsonify(dlist)

@app.route('/students',methods=['POST'])
def createStudent():
    
    temp = Student(**request.json)
    db.session.add(temp)
    db.session.commit()
    return jsonify(temp.to_dict())


@app.route('/students/<studentName>')
def viewStudent(studentName):
    res = Student.query.filter_by(name = studentName ).first_or_404()
    d = res.to_dict()
    return jsonify(d)

@app.route('/students/<studentName>',methods=['DELETE'])
def deleteStudent(studentName):
    res = Student.query.filter_by(name = studentName ).first_or_404()
    db.session.delete(res)
    db.session.commit()
    return jsonify({'message' : 'Success!'})

@app.route('/blogs')
def viewAllBlogs():
    res = Blog.query.all()
    dlist=[r.to_dict() for r in res]
    print(dlist)
    return jsonify(dlist)

@app.route('/blogs/<int:author>',methods=['POST'])
def createBlog(author):
    temp = Blog(**request.json)
    temp.author = author
    db.session.add(temp)
    db.session.commit()
    return jsonify(temp.to_dict())

@app.route('/blogs/<int:author>')
def viewBlog(author):
    res = Blog.query.filter_by(author=author)
    dlist=[r.to_dict() for r in res]
    print(dlist)
    return jsonify(dlist)


if __name__ == '__main__':
    app.run(debug=True)

