from app import db
from app.models import User, Enrollment
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload

class SelectWrapper:
    def __init__(self, model_class, *expressions, joins=None):
        self.model_class = model_class
        self.expressions = expressions
        self.joins = joins or []

    # def statement(self):
    #     return select(self.model_class).where(*self.expressions)

    def statement(self):
        stmt = select(self.model_class)
        for relation in self.joins:
            stmt = stmt.join(getattr(self.model_class, relation))
        if self.expressions:
            stmt = stmt.where(*self.expressions)
        return stmt


    def one_or_none(self):
        return db.session.execute(self.statement()).scalar_one_or_none()

    def all(self):
        return db.session.execute(self.statement()).scalars().all()

    def first(self):
        return db.session.execute(self.statement()).scalars().first()

    def count(self):
        return len(self.all())


# TODO: thinking of using this in the future
# def get_model_from_expression(expr):
#     # Stable in SQLAlchemy 2.x, but not guaranteed in future versions
#     return expr.left._annotations['parententity']


# Usage example: select_where(User.email == "test@example.com").one_or_none()
def select_where(*expressions : BinaryExpression):
    column = expressions[0].left
    model = column._annotations['parententity'] # voodoo
    return SelectWrapper(model, *expressions)


# Usage example: delete_where(User.email == "student@mail.com") 
# Does not cascade, might be useful too
def delete_where(*expressions : BinaryExpression):
    column = expressions[0].left
    model = column._annotations['parententity'] # voodoo
    stmt = delete(model).where(*expressions)
    db.session.execute(stmt)
    db.session.commit()

# Usage example: delete_where_cascade(User.email == "student@mail.com") 
# Does cascade, means it will delete all related objects,
# based on defined cascade logic.
def delete_where_cascade(*expressions: BinaryExpression):
    column = expressions[0].left
    model = column._annotations['parententity'] # voodoo
    objects = db.session.scalars(select(model).where(*expressions)).all()
    for obj in objects:
        db.session.delete(obj)
    db.session.commit()


# Usage example: update_where(User.email == "student@mail.com", {"name": "Alice"})
def update_where(*expressions: BinaryExpression, values: dict):
    if not expressions:
        raise ValueError("No conditions provided to update_where()")
    
    column = expressions[0].left
    model = column._annotations['parententity'] # voodoo

    stmt = update(model).where(*expressions).values(**values)
    db.session.execute(stmt)
    db.session.commit()

# Usage example: update_where_cascade(User.email == "student@mail.com", {"name": "Alice"})
def update_where_cascade(*expressions: BinaryExpression, values: dict):
    column = expressions[0].left
    model = column._annotations['parententity']
    objects = db.session.scalars(select(model).where(*expressions)).all()
    for obj in objects:
        for key, val in values.items():
            setattr(obj, key, val)
    db.session.commit()



# Usage example: get_any_user_full_info("student@mail.com")
def get_user_full_info(email: str) -> User:
    return db.session.query(User).options(
        joinedload(User.program),
        joinedload(User.group),
        joinedload(User.enrollments).joinedload(Enrollment.module),
        joinedload(User.modules_taught)
    ).filter_by(email=email).first()

# or could use just :
# user = User.query.filter_by(email='student@mail.com').first()
# and then user.program.name
