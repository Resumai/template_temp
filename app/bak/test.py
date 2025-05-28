
# # def shout(var):
# #     def decorator(var):
# #         print("Before!")
# #         print(var)
# #         print("After!")
# #     return decorator

# # @shout
# # def greet(name):
# #     return f"Hello, {name}!"


# # greet("Mantas")


# def shout(var):
#     print("Before!")
#     print(var())
#     print("After!")
#     return var

# @shout
# def test():
#     return "Mantas"

# # test()
# print(test())


# from app import User

# def query_or_none(column, value):
#     model = column.class_
#     stmt = select(model).where(column == value)
#     return db.session.execute(stmt).scalar_one_or_none()

# user = query_or_none(User.email, "test@example.com")
# print(user)

def other_func(var):
    print(var)

# def my_func():
#     return "Dude"

other_func("Dude")

# from sqlalchemy import Column, Integer,  String, select, update, delete, DateTime, ForeignKey


# class TextTest:
#     text = "test@example.com"

#     def __eq__(self, other):
#         return self.text == other

# test = TextTest()

class User:
    email = "test@example.com"

    def __eq__(self, other):
        return self.email == other

def select_where(*args):
    for expression in args:
        print("Received:", expression)

select_where(User.email == "test@example.com")