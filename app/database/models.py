from enum import Enum
from tortoise import fields, models

"""Model definition

Initial setup: 
docker-compose exec backend aerich init -t database.config.TORTOISE_ORM
docker-compose exec backend aerich init-db

To sync the model definition with database: 
docker-compose exec backend aerich migrate
docker-compose exec backend aerich upgrade

"""

# TODO: alternative Pony ORM

class NoteStatusEnum(str, Enum):
    active = "active"
    completed = "complete"
    deleted = "deleted"

class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

class Notes(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    content = fields.TextField()
    status: NoteStatusEnum = fields.CharEnumField(NoteStatusEnum, max_length=8, default=NoteStatusEnum.active)
    author = fields.ForeignKeyField("models.Users", related_name="note")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"