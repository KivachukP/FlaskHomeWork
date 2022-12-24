from flask import Flask, render_template, request
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)



    def __repr__(self):
        return '<Article %r>' % self.id
with app.app_context():
    db.create_all()




@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')



@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/dashboard/<name>')
def dashboard(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      return redirect(url_for('dashboard',name = user))
   else:
      user = request.args.get('name')
      return render_template('login.html')


@app.route('/blog')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("page2.html", articles=articles)




@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/blog')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


@app.route('/blog/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)

@app.route('/blog/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/blog')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        article = Article.query.get(id)
        return render_template("update_article.html", article=article)

@app.route('/blog/<int:id>/delete')
def posts_detail_del(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/blog')
    except:
        return "При удалении статьи произошла ошибка"



if __name__=='__main__':
    app.run(debug=True)
