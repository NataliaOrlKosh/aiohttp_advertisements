from aiohttp import web
from gino import Gino
from asyncpg.exceptions import UniqueViolationError
from datetime import datetime
import hashlib


db = Gino()


class BaseModel:

    @classmethod
    async def get_or_404(cls, id):
        instance = await cls.get(id)
        if instance:
            return instance
        raise web.HTTPNotFound()

    @classmethod
    async def create_instance(cls, **kwargs):
        try:
            instance = await cls.create(**kwargs)
        except UniqueViolationError:
            raise web.HTTPBadRequest()
        return instance


class User(db.Model, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), unique=True)

    def to_dict(self):
        user_data = super().to_dict()
        user_data.pop('password')
        return user_data

    @classmethod
    async def create_instance(cls, **kwargs):
        kwargs['password'] = hashlib.md5(kwargs['password'].encode()).hexdigest()
        return await super().create_instance(**kwargs)

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'


class Advertisement(db.Model, BaseModel):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    author = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, *args, **kwargs):
        super(Advertisement, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Advertisement {self.id} - {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text
        }