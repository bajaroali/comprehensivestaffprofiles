#import the create_app application factory
from app import create_app
from app.models import db, User,Role, Employee

# import the application config classes
from config import DevelopmentConfig, ProductionConfig, TestingConfig


#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == '__main__':
    app.run()
