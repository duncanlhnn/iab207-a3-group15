from flask import Flask
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicfestival.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from views.routes import routes  
    app.register_blueprint(routes)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() 
    app.run(debug=True)


