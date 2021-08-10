db.createUser(
        {
            user: "flask_user",
            pwd: "flask_user_password",
            roles: [
                {
                    role: "readWrite",
                    db: "user_db"
                }
            ]
        }
);