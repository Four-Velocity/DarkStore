__all__ = [
    "User",
    "ProfileCurrency"
]

from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=50)

    @property
    def is_admin(self) -> bool:
        return self.full_name == "admin"

    def __str__(self):
        return str(self.full_name)


class ProfileCurrency(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="currencies")
    name = fields.CharField(max_length=5)
    amount = fields.DecimalField(max_digits=22, decimal_places=11)

    class Meta:
        unique_together = ("user", "name")

    class PydanticMeta:
        exclude = ["id"]

    def __str__(self):
        try:
            return f"{self.user.full_name}'s {self.name}"
        except (TypeError, AttributeError):
            return self.name
