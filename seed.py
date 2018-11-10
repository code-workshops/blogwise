import random
from models import *
from faker import Faker

fake = Faker()


def generate_data():
    User.query.delete()
    Article.query.delete()

    # Create 5 users ...
    for _ in range(5):
        user = User(name=fake.name(), password=fake.password())
        db.session.add(user)
        # User must be commited! Or it won't have an id to assign it to Author
        db.session.commit()

        # Each user should have 7 articles ...
        for i in range(7):
            article = Article(author_id=user.id,
                              title=' '.join(fake.words(nb=random.randrange(1, 3))).capitalize(),
                              content='\n\n'.join(fake.paragraphs(nb=4)))
            db.session.add(article)
        db.session.commit()


if __name__ == '__main__':
    # An application context is required to connect to the database!
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    generate_data()
    print('Database seeding complete.')
