# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/signUp.ipynb (unless otherwise specified).

__all__ = ['UserInput', 'H', 'signUp']

# Cell
from .userTable import UserTable
from awsSchema.apigateway import Response, Event
from copy import deepcopy
from beartype import beartype
from uuid import uuid4
from .saltHashPassword import hash_password, check_password
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from time import time

# Cell
@dataclass_json
@dataclass
class UserInput:
    username: str
    password: str

    @property
    def passwordHash(self):
        return hash_password(self.password)

    def saveTable(self):
        passwordHashed = self.passwordHash
        userTable = UserTable(
                userId = str(uuid4()),
                username = self.username,
                date = time(),
                passwordHash = passwordHashed
            )
        userTable.save()


# Cell
class H:
    class ParseInputError(Exception): pass
    class SavingError(Exception): pass
    @classmethod
    @beartype
    def parseInput(cls, event:dict)->UserInput:
        try:
            user = Event.parseDataClass(UserInput, deepcopy(event))
            return user
        except Exception as e:
            raise cls.ParseInputError(e)

    @classmethod
    @beartype
    def saveUserMethod(cls, user:UserInput)->bool:
        try:
            user.saveTable()
            return True
        except Exception as e:
            raise cls.SavingError(e)



# Cell
def signUp(event, *args):
    try:
        user = H.parseInput(event)
        print(user.username)
        H.saveUserMethod(user)
        return Response.returnSuccess()
    except H.SavingError as e:
        return Response.returnError(f'failed saving user {e}')
    except Exception as e:
        return Response.returnError(f' unknown error {e}')
