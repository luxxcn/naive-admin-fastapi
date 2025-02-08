DEBUG = True

# jwt secret key
SECRET_KEY = "abcdb1e7e7b1b1e7e7b1b1e7e7b1b1e7e7b11"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30 * 24 * 60

# 数据库uri
DATABASE_URI = "mysql+pymysql://root:password@localhost:3306/naive-admin-fastapi"
