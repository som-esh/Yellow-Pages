from flask import Flask, render_template, redirect, request
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:toor@localhost:5432/postgres"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()

# conn = psycopg2.connect("postgresql://postgres:toor@localhost:5432/postgres")
# cur = conn.cursor()
# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")


class Detail(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(20), nullable=False)
    number = db.Column(db.String(10), nullable=False)

    # def __init__(self, name, mail, number):
    #     self.name = name
    #     self.mail = mail
    #     self.number = number

    def __repr__(self):
        return '<Detail %r' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['mail'])
        print(request.form['number'])

        # data = request.get_json()

        name = request.form['name']
        mail = request.form['mail']
        number = request.form['number']

        new_contact = Detail(name=name, mail=mail, number=number)

        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect('/')

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return 'Error while adding to database'

    return render_template('create.html')


@app.route('/view', methods=['POST', 'GET'])
def view():
    details = Detail.query.order_by(Detail.id).all()
    return render_template('view.html', details=details)


@app.route('/delete/<int:id>')
def delete(id):
    detail_to_delete = Detail.query.get_or_404(id)

    try:
        db.session.delete(detail_to_delete)
        db.session.commit()
        return redirect('/view')
    except:
        return 'Cannot delete entry from database'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    detail_to_update = Detail.query.get_or_404(id)
    if request.method == 'POST':
        detail_to_update.name = request.form['name']
        detail_to_update.mail = request.form['mail']
        detail_to_update.number = request.form['number']

        try:
            db.session.commit()
            return redirect('/view')

        except:
            return 'Error while updating'
    else:
        return render_template('update.html', details=detail_to_update)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']

        object = Detail.query.filter_by(name=name).first()
        if object is not None:
            if (object.name == name and object.mail == mail):
                return render_template('display.html', details=object)
            else:
                return 'Not Found'
        else:
            return 'Not Found'

    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
