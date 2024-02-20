from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite'
db = SQLAlchemy(app)

class Myapp(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(500))

@app.route('/')
def home():
    return redirect(url_for('home1'))

@app.route('/insert', methods=['POST'])
def home2():
    c_name = request.form.get("c_name")
    new_c_name = Myapp(c_name=c_name)
    db.session.add(new_c_name)
    db.session.commit()
    return redirect(url_for("home1"))

@app.route('/delete/<int:c_id>')
def delete(c_id):
    c_name_to_delete = Myapp.query.get_or_404(c_id)
    db.session.delete(c_name_to_delete)
    db.session.commit()
    return redirect(url_for("home1"))

@app.route('/base')
def home1():
    my_list = Myapp.query.all()
    return render_template('base.html', my_list=my_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
