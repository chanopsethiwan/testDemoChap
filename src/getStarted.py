# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/getStarted.ipynb (unless otherwise specified).

__all__ = ['GetStartedInput', 'H', 'getStarted']

# Cell
from .userTable import UserTable
from awsSchema.apigateway import Response, Event
from copy import deepcopy
from .saltHashPassword import hash_password, check_password
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from beartype import beartype

# Cell
@dataclass_json
@dataclass
class GetStartedInput:
    username: str
    fullname: str
    nickname: str
    levelOfStudy: str


# Cell
class H:
    class ParseInputError: pass
    class GetStartedError: pass

    @classmethod
    @beartype
    def parseInput(cls, event:dict)->GetStartedInput:
        try:
            user = Event.parseDataClass(GetStartedInput, deepcopy(event))
            return user
        except Exception as e:
            raise cls.ParseInputError(e)

    @classmethod
    @beartype
    def getStartedInfo(cls, user: GetStartedInput):
        try:
            usernameQuery = UserTable.username_index.query(user.username)
            for i in usernameQuery:
                userId = i.userId
                oldItem = UserTable.get(userId)
                oldItem.fullname = user.fullname
                oldItem.nickname = user.nickname
                oldItem.levelOfStudy = user.levelOfStudy
                oldItem.save()
        except Exception as e:
            raise cls.GetStartedError
        return True

# Cell
def getStarted(event, *args):
    try:
        user = H.parseInput(event)
        H.getStartedInfo(user)
        return Response.returnSuccess()
    except H.ParseInputError as e:
        return Response.returnError(f'failed to parse input {e}')
    except H.GetStartedError as e:
        return Response.returnError(f'failed to save get started information {e}')