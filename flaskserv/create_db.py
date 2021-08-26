from flaskserv.socialnet import db, create_app

from flaskserv.socialnet.auth.model import User
app = create_app()
app.app_context().push()
db.drop_all(app=app)
db.create_all(app=app)


for name in ("Alice", "Bob", "Carol"):
    user = User(name=name,
                email=f"{name}@example.com",
                password="bad_password")
    db.session.add(user)
db.session.commit()





