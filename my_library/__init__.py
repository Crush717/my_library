import pymysql

# 解决 ModuleNotFoundError: No module named 'MySQLdb' 错误：https://blog.csdn.net/m0_37886429/article/details/83540314
pymysql.install_as_MySQLdb()