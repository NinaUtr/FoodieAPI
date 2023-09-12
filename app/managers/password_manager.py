from passlib.context import CryptContext


class PasswordManager:
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.PWD_CONTEXT.hash(password)


password_manager = PasswordManager()
