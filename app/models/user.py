from flask import current_app
from app import db,login_manager,app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.models.post import Post
from app.models.follower import followers 

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique = True, nullable = False)
    email = db.Column(db.String(50),unique = True,nullable = False)
    password = db.Column(db.String(100),nullable = False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username) + ' <Email {}>'.format(self.email)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())    

def getUser(username):
    return User.query.filter_by(username=username).first_or_404()