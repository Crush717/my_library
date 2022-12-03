from enum import Enum


class Sex(Enum):
  """性别枚举
  """
  male = {'value': 1, 'label': '男'}
  female = {'value': 2, 'label': '女'}
