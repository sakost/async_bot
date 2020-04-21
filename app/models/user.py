from tortoise.models import Model
from tortoise import fields


class UserModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(db_index=True, max_length=255, null=False)
    surname = fields.CharField(db_index=True, max_length=255, null=False)

    class Meta:
        table = 'user'

    def __str__(self):
        return f"<User(id={self.id}, name={self.name}, surname={self.surname})>"

    __repr__ = __str__


class SettingsModel(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(index=True, max_length=255, null=False)
    value = fields.TextField(null=True)
    owner: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        'models.UserModel', related_name='settings'
    )

    class Meta:
        table = 'settings'

    def __str__(self):
        return f'<User(id={self.id}, key={self.key}, value={self.value})>'
