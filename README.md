**Add the `.env` file with the following settings:**

```bash
#PostgreSQL Date Base
SQLALCHEMY_DATABASE_URL=
#Authentication and token generation
SECRET_KEY=
ALGORITHM=
#Email config
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=
MAIL_FROM_NAME=
MAIL_STARTTLS=
MAIL_SSL_TLS=
USE_CREDENTIALS=
VALIDATE_CERTS=
#Docker-compose Redis
REDIS_HOST=
REDIS_PORT=
REDIS_DB=
#Docker-compose Postgres
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=
#Cloudinary
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

---

**Note:** Ensure to keep your `.env` file secure and never commit it to the repository to protect sensitive information.

---