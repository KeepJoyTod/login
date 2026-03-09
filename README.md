# FastAPI JWT Auth API

## 技术栈
- Python 3.11+
- FastAPI 0.110+
- SQLAlchemy 2.0 ORM
- PostgreSQL 15+
- python-jose
- passlib[bcrypt]
- Pydantic 2.x
- Alembic

## 启动
1. 安装依赖
```bash
pip install -r requirements.txt
```
2. 配置环境变量
```bash
copy .env.example .env
```
3. 启动服务
```bash
uvicorn app.main:app --reload
```

## 接口
- 注册接口：`POST /api/v1/auth/register`
- 登录接口：`POST /api/v1/auth/login`
- 鉴权示例接口：`GET /api/v1/users/me`

请求体示例：
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "StrongPass123",
  "phone": "13800000000"
}
```

响应示例：
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer",
  "user_id": 1
}
```

登录请求体示例：
```json
{
  "username": "alice",
  "password": "StrongPass123"
}
```

登录失败示例：
```json
{
  "detail": "用户名或密码错误"
}
```

## Swagger 测试说明
1. 打开 `http://127.0.0.1:8000/docs`
2. 先调用 `POST /api/v1/auth/register` 注册用户
3. 再调用 `POST /api/v1/auth/login` 获取 `access_token`
4. 点击右上角 `Authorize`，输入 `Bearer <access_token>` 后授权
5. 调用 `GET /api/v1/users/me`，验证返回当前用户信息
6. 连续错误登录超过限制后，验证 5 分钟内最多 5 次尝试

JWT 解码验证示例：
```python
from jose import jwt

SECRET_KEY = "PLEASE_REPLACE_WITH_LONG_RANDOM_SECRET"
ALGORITHM = "HS256"
token = "xxx.jwt.xxx"

payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print(payload["sub"], payload["username"], payload["exp"])
```

ReDoc 地址：`http://127.0.0.1:8000/redoc`

## Alembic 迁移预留
- 自动迁移文件目录：`alembic/versions`
- 生成迁移：
```bash
alembic revision --autogenerate -m "init users table"
```
- 执行迁移：
```bash
alembic upgrade head
```
