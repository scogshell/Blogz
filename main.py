from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    
@app.route('/request',method=[GET,POST])
def add_blog(): 


    return render_template

@app.route(/blog', methods=GET,POST]))
def index(): A
    blog_id =request.args.get("id")
    blog= Blog.query.get(blog_id)

    return ren'der_template('blogentry.html',blog=blog)
else:
    blogs=Blog.query.all()

    return render_template('blog.html', title= 'build A Blog", blogs=')

@app.route('/newpost')


app.route('/', methods=['POST', 'GET'])
def index():

      if request.method == 'POST':
  #      task = request.form['task']
  #      tasks.append(task)

#return render_template('todos.html',title="", tasks=tasks)





#if __name__ == '__main__':
#app.run()