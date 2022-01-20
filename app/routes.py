from app import app
from flask import render_template, redirect, flash
from flask import url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import *
from app.models import User, users


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = TaskForm()

    if form.validate_on_submit():

        toDo = current_user.tasks
        idx = 1 if not toDo else max(toDo.keys()) + 1

        toDo[idx] = {'text': form.task.data,
                     'done': False,
                     'description': form.description.data,
                     'due': form.due.data}

        return redirect(url_for('main'))

    else:
        return render_template("addtask.html", form=form)


@app.route("/")
def main():
    if current_user.is_authenticated:
        toDo = current_user.tasks
        return render_template("tasks.html", tasks=toDo)
    else:
        return redirect(url_for('login'))


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
@login_required
def edit(id):

    toDo = current_user.tasks
    if not(id in toDo):
        flash('Trying to edit an unknown task', 'warning')
        return redirect(url_for('main'))

    task = toDo[id]
    form = TaskForm()

    if form.validate_on_submit():
        task['text'] = form.task.data
        task['description'] = form.description.data
        task['due'] = form.due.data

        return redirect(url_for('main'))

    else:
        form.due.data = task['due']
        form.description.data = task['description']
        form.task.data = task['text']
        return render_template("edittask.html", form=form, id=id)


@app.route("/toggle/<int:id>")
@login_required
def toggle(id):
    toDo = current_user.tasks
    if not(id in toDo):
        flash('Trying to change an unknown task', 'warning')
        return redirect(url_for('main'))

    task = toDo[id]
    task['done'] = not task['done']

    return redirect(url_for('main'))


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    toDo = current_user.tasks
    if not(id in toDo):
        flash('Trying to delete an unknown task', 'warning')
        return redirect(url_for('main'))

    del toDo[id]

    return redirect(url_for('main'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('main'))

    form = LoginForm()

    # Check if it is a POST request an if it is valid
    if form.validate_on_submit():
        user = next((x for x in users if form.username.data == x.get_username()
                     and form.password.data == x.get_password()), None)

        if user is not None:
            if user.blocked:
                flash('Blocked user', 'danger')
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('main'))

        else:
            flash('Wrong username or password', 'warning')
            return redirect(url_for('login'))

    # If GET method
    else:
        return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('main'))

    form = RegisterForm()
    print(form.birth.data)

    if form.validate_on_submit():
        new = User(form.username.data, form.last_name.data,
                   form.first_name.data, form.birth.data, form.password.data)

        users.append(new)
        return redirect(url_for('login'))

    else:
        return render_template('register.html', form=form)


@app.route("/admin")
@login_required
def admin():
    if current_user.group == 'admin':
        return render_template('admin.html', users=users)

    else:
        flash('You are not an admin', 'warning')
        return redirect(url_for('main'))


@app.route("/admin/ch-block/<string:user>")
@login_required
def block(user):
    if not current_user.group == 'admin':
        flash('You are not an admin', 'warning')
        return redirect(url_for('main'))

    u = next((x for x in users if user == x.get_username()), None)

    if u is None:
        return redirect(url_for('admin'))

    u.blocked = not u.blocked
    return redirect(url_for('admin'))


@app.route("/admin/ch-group/<string:user>")
@login_required
def group(user):
    if not current_user.group == 'admin':
        flash('You are not an admin', 'warning')
        return redirect(url_for('main'))

    u = next((x for x in users if user == x.get_username()), None)

    if u is None:
        return redirect(url_for('admin'))

    u.group = 'admin' if u.group == 'normal' else 'normal'
    return redirect(url_for('admin'))
