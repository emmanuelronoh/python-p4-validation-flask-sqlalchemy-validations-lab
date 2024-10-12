from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        if phone_number and not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)  # Make content required
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        if self.is_clickbait(title):
            raise ValueError("Title cannot be clickbait.")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary cannot exceed 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Technology', 'Health', 'Lifestyle']  # Example categories
        if category and category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

    @staticmethod
    def is_clickbait(title):
        clickbait_phrases = [
            "You Won't Believe What Happens Next!",
            "Top [number] Reasons",
            "Why You Should",
            "The Secret to",
            "How to",
            "This One Simple Trick",
            # Add more phrases as needed
        ]
        return any(phrase in title for phrase in clickbait_phrases)

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
