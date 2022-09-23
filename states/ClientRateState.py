from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.helper import Helper, HelperMode, ListItem


class GetFeedBack(StatesGroup):

    NAME = State()
    PHONE = State()
    RATE = State()


if __name__ == '__main__':
    print(GetFeedBack)
    pass
