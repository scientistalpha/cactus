from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean)


@app.route("/homie", methods=["POST"])
def homie():

    todo_list = Todo.query.all()

    # false number to know how many unfinished tasks

    return render_template("base.html",  todo_list=todo_list)


@app.route('/')
def home():
    todo_list = Todo.query.all()
    false_number = 0
    for elements in todo_list:
        if elements.complete == False:
            false_number += 1
    return render_template("base.html", false_number=false_number, todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)

    db.session.add(new_todo)

    db.session.commit()

    return redirect(url_for("home"))


@app.route('/update/<int:todo_id>', methods=['GET', 'POST'])
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if request.method == 'POST':

        try:
            todo.title = request.form['content']
            db.session.commit()

            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', todo_id=todo_id, todo=todo)


@app.route("/change/")
def change():

    return render_template('change.html')


@app.route("/check/<int:todo_id>")
def check(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
