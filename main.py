from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:1234@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = '1234567890'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blog_id = db.relationship('Blog', backref ='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password 
        
@app.before_request
def require_login():
    if 'username' not in session:
        allowed_routes = ['signup', 'login', 'index','blog']
        if request.endpoint not in allowed_routes and 'username' not in session:
            return  redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash(user.username + ", is logged in")
            return redirect('/newpost')
        
        if not user:  
            flash('Hmmm, We dont have a user with that username. Please sign up below')
            return redirect ('/login')
        
        if user and user.password != password:
            flash('Hmmm, Whats up Doc? Think you typed the wrong password.')
            
        if len(password) < 1:
            flash("Forget something?")

    return render_template('login.html')
        
      
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        #existing user hey u already have an acct
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash( "User already exist")
            return redirect('/login')

        #signup errors
        if len(username) < 1:
            flash("Now you know blank is not a username. try again. ")
        if len(password) < 1:
            flash("Cmon now...Invalid password")
        if len(verify) <1:
            flash("Cant leave this blank either.")
            return redirect ('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
                
        
        
        #sign them up for an acct if they dont have one w/user name
        #store username in session  
        if not existing_user:
                        
            new_user = User(username, password,)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash(new_user.username + ", is logged in")
            return redirect('/newpost')
     
        
        
       
    return render_template ('signup.html')



@app.route('/blog', methods=['GET', 'POST'])
def blog():

    blog_id = request.args.get("id")
    owner_name = request.args.get('user')
    
    
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('newblog.html', blog=blog)
    if owner_name is not None:
        userid = User.query.filter_by(username=owner_name).first().id
        user_blogs = Blog.query.filter_by(owner_id=userid).all()
        return render_template('singleUser.html', title="Written by:", user_blogs=user_blogs)

    else: 
        blogs = Blog.query.all()

        return render_template("blog.html", blogs=blogs)

#@app.route('/blog', methods=['GET'])    
#def blog():
   #blog_id = request.args.get("id")
   #if request.args:
       #blog = Blog.query.get(blog_id)

       #return render_template('newblog.html', blog=blog)
   #else:
       #blogs = Blog.query.all()

       #return render_template('blog.html', title="Blogz", blogs=blogs)

@app.route('/', methods=['POST', 'GET'])
def index():
    
    users = User.query.all()
    return render_template('index.html', users = users)



@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'GET':
        return render_template('newpost.html', title='Add Blog Entry')

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        title_error = ""
        body_error = ""

        if len(blog_title) < 1:
            title_error = "Hey you forgot to title this blog!"
            blog_title=""
        
        if len(blog_body) < 1:
            body_error = "So whats your blog about?"
            blog_body =""
        
        if title_error:
            return render_template('newpost.html', blog_body=blog_body, title_error=title_error)
        if body_error:
            return render_template('newpost.html',blog_title=blog_title, body_error=body_error)                
        
        if not title_error and not body_error:
            #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            #blog_id = db.relationship('Blog', backref ='owner')
           
           
            new_blog = Blog(blog_title, blog_body, owner)
            
            db.session.add(new_blog)
            db.session.commit()
            newb = Blog.query.all()           
            newbid = str(new_blog.id)
            
            return redirect ( "/blog?id=" + newbid)
        else:
            return render_template('newpost.html', title="Add Blog Entry", title_error=title_error, body_error=body_error, blog_title=blog_title, blog_body=blog_body)






if __name__=='__main__':
    app.run()    















