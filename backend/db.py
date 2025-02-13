import src.app as app


if __name__ == '__main__':
    Base = app.database.Base
    engine = app.database.engine
    Base.metadata.create_all(engine)
