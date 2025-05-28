from app import db
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import select

# TODO: move to utils or smth
class SelectWrapper:
    def __init__(self, model_class, *expressions):
        self.model_class = model_class
        self.expressions = expressions

    def statement(self):
        return select(self.model_class).where(*self.expressions)

    def one_or_none(self):
        return db.session.execute(self.statement()).scalar_one_or_none()

    def all(self):
        return db.session.execute(self.statement()).scalars().all()

    def first(self):
        return db.session.execute(self.statement()).scalars().first()

    def count(self):
        return len(self.all())




def select_where(*expressions : BinaryExpression):
    column = expressions[0].left
    model = column._annotations['parententity'] # voodoo
    return SelectWrapper(model, *expressions)