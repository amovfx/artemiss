from flaskserv.socialnet import db, create_app

from flaskserv.socialnet.models import User, Tribe, Post
from flaskserv.socialnet.config import DevelopmentConfig
app = create_app()
app.app_context().push()
db.drop_all(app=app)
db.create_all(app=app)

users = []
for name in ("Alice", "Bob", "Carol"):
    user = User(name=name,
                email=f"{name}@example.com",
                password="bad_password")

    db.session.add(user)
    users.append(user)

post = Post(title = "First Post",
            message = "Life is good, life is progress.",
            owner = users[1])
db.session.add(post)
db.session.commit()

print( db.session.query(User)[0:10] )





