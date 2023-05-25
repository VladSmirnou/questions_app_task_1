from environs import Env


env = Env()
env.read_env()

class Config:
    FLASK_APP=env.str('FLASK_APP')
    FLASK_DEBUG = env.bool('FLASK_DEBUG', default=False)
    SQLALCHEMY_DATABASE_URI=env.str('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=env.bool('SQLALCHEMY_TRACK_MODIFICATIONS', default=False)
