import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from models import db, Author, Post
import logging
from faker import Faker

LOGGER = logging.getLogger(__name__)

class TestAuthor:
    '''Class Author in models.py'''

    def test_requires_name(self):
        '''Requires each record to have a name.'''
        with app.app_context():
            # Valid name
            author1 = Author(name=Faker().name(), phone_number='1231144321')

            # Missing name
            with pytest.raises(ValueError):
                Author(name='', phone_number='1231144321')

    def test_requires_unique_name(self):
        '''Requires each record to have a unique name.'''
        with app.app_context():
            db.session.query(Author).delete()
            db.session.commit()

            author_a = Author(name='Ben', phone_number='1231144321')
            db.session.add(author_a)
            db.session.commit()

            # Trying to add a duplicate author
            with pytest.raises(IntegrityError):
                author_b = Author(name='Ben', phone_number='9876543210')
                db.session.add(author_b)
                db.session.commit()

            db.session.rollback()  # Rollback to keep the session clean after the exception

    def test_requires_ten_digit_phone_number(self):
        '''Requires each phone number to be exactly ten digits.'''
        with app.app_context():
            with pytest.raises(ValueError):
                LOGGER.info('Testing short phone number')
                Author(name="Jane Author", phone_number="3311")

            with pytest.raises(ValueError):
                LOGGER.info("Testing long phone number")
                Author(name="Jane Author", phone_number="3312212121212121")

            with pytest.raises(ValueError):
                LOGGER.info("Testing non-digit")
                Author(name="Jane Author", phone_number="123456789!")

class TestPost:
    '''Class Post in models.py'''

    def test_requires_title(self):
        '''Requires each post to have a title.'''
        with app.app_context():
            with pytest.raises(ValueError):
                content_string = "HI" * 126
                Post(title='', content=content_string, category='Technology')  # Use a valid category

    def test_content_length(self):
        '''Content too short test. Less than 250 chars.'''
        with app.app_context():
            # Valid content length
            content_string1 = 'A' * 250
            Post(title='Secret Why I love programming.', content=content_string1, category='Technology')  # Use a valid category
            
            with pytest.raises(ValueError):
                # Too short
                content_string2 = 'A' * 249
                Post(title='Guess Why I love programming.', content=content_string2, category='Technology')  # Use a valid category

    def test_summary_length(self):
        '''Summary too long test. More than 250 chars.'''
        with app.app_context():
            content_string = "A" * 250
            
            # Valid summary string
            summary_string1 = "T" * 250
            Post(title='You Won\'t Believe Why I love programming..', content=content_string, summary=summary_string1, category='Technology')  # Use a valid category
            
            # Too long
            summary_string2 = "T" * 251
            with pytest.raises(ValueError):
                Post(title='Top Reasons Why I love programming..', content=content_string, summary=summary_string2, category='Technology')  # Use a valid category

    def test_category(self):
        '''Incorrect category test.'''
        with app.app_context():
            content_string = "A" * 251
            with pytest.raises(ValueError):
                Post(title='Top Ten Reasons I Love Programming.', content=content_string, category='Banana')  # Invalid category

    def test_clickbait(self):
        '''Test clickbait validator for title.'''
        with app.app_context():
            content_string = "A" * 260  # Valid content length
            with pytest.raises(ValueError):
                Post(title='You Won\'t Believe What Happens Next!', content=content_string, category='Technology')  # Clickbait title
