from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, name, first_name, birth, password, group="normal", blocked=False, tasks=None):
        if tasks is None:
            tasks = {}
        self.id = id
        self.name = name
        self.first_name = first_name
        self.birth = birth
        self.password = password
        self.group = group
        self.blocked = blocked
        self.tasks = tasks

    def get_username(self):
        return self.id

    def get_password(self):
        return self.password


users = [User(id="root", name="The", first_name="Root", birth="1900-01-01", password="root", group='admin')]
from app import login_manager


# callback to reload the user object
@login_manager.user_loader
def load_user(username):
    return next((x for x in users if username == x.get_username()), None)
