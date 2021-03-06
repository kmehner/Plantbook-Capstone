from app import db
from datetime import datetime
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api


cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    body = db.Column(db.String(255))
    water_quantity = db.Column(db.Integer)
    water_measurement = db.Column(db.String(50))
    frequency_int = db.Column(db.Integer)
    frequency_measurement = db.Column(db.String(50))
    category = db.Column(db.String(50))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_url = db.Column(db.String(100))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Post|{self.title}>"

    def update(self, **kwargs):
        for key, value in kwargs.items(): # added update for new variables 
            if key in {'title', 'body', 'water_quantity', 'water_measurement', 'frequency_int', 'frequency_measurement'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        if self.image_url:
            self.delete_from_cloudinary
        db.session.delete(self)
        db.session.commit()

    def upload_to_cloudinary(self, file_to_upload):
        image_info = cloudinary.uploader.upload(file_to_upload)
        self.image_url = image_info.get('url')
        db.session.commit()

    def delete_from_cloudinary(self):
        p_id = self.image_url.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(p_id)
        db.session.commit()


# need to remove unique constraint - error but is created 
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(50), nullable=False)
    scientific_name = db.Column(db.String(50))
    content = db.Column(db.String(200))
    posts = db.relationship('Post', backref='plant', lazy='dynamic')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_url = db.Column(db.String(100))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Plant|{self.common_name}>"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'common_name', 'scientific_name', 'content'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        if self.image_url:
            self.delete_from_cloudinary
        db.session.delete(self)
        db.session.commit()

    def upload_to_cloudinary(self, file_to_upload):
        image_info = cloudinary.uploader.upload(file_to_upload)
        self.image_url = image_info.get('url')
        db.session.commit()

    def delete_from_cloudinary(self):
        p_id = self.image_url.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(p_id)


# Bookmark Plant class here 
# Example in ultimate flask tutorial
# Want to be able to save plant to my page

# Bookmark Post class here 
# Want to be able to save posts from community page here 

class PlantBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()