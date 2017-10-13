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

@app.route('/blog', methods=['GET', 'POST'])
def blog():

    
    blog_id = request.args.get("id")
    if request.args:
        blog = Blog.query.get(blog_id)
        return render_template('newblog.html', blog=blog)

    else:
        blogs = Blog.query.all()

        return render_template('blog.html', title="Build A Blog", blogs=blogs)



@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'GET':
        return render_template('newpost.html', title='Add Blog Entry')

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ""
        body_error = ""

        if len(blog_title) < 1:
            title_error = "Hey you forgot to title this blog!"

        if len(blog_body) < 1:
            body_error = "So whats your blog about?"

        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            newb = Blog.query.all()           
            newbid = str(new_blog.id)

            return redirect ( "/blog?id=" + newbid)
        else:
            return render_template('newpost.html', title="Add Blog Entry", title_error=title_error, body_error=body_error)


if __name__=='__main__':
    app.run()    
