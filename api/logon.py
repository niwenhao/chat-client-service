from db.model import Session, User

from pydantic import BaseModel
import hashlib

from fastapi import APIRouter

router = APIRouter()


class PostUser(BaseModel):
    name: str
    password: str

@router.post("/logon")
async def logon(user: PostUser):
    # Create a new md5 hash object
    hash_object = hashlib.md5(user.password.encode())

    # Get the hexadecimal representation of the hash
    enc_password = hash_object.hexdigest()

    with Session() as session:
        # Select the user from the database using username
        user = session.query(User).filter_by(name=user.name).first()
        if user is None:
            return {"status": "failed", "message": "User not found"}
        else:
            if user.password == enc_password:
                return {"status": "success", "id": user.id, "name": user.name}
            else:
                return {"status": "failed", "message": "Password incorrect"}

# A API To create a new user with user name and password.
# and encode the password using md5 hash and save it to the database.
@router.post("/users")
async def create_user(user: PostUser):
    # Create a new md5 hash object
    hash_object = hashlib.md5(user.password.encode())

    # Get the hexadecimal representation of the hash
    enc_password = hash_object.hexdigest()

    with Session() as session:
        # Create a new user
        new_user = User(name=user.name, password=enc_password)
        session.add(new_user)
        session.commit()
        return {"status": "success", "id": new_user.id, "name": new_user.name}

# A API to list all users in the database
@router.get("/users")
async def list_users():
    with Session() as session:
        users = session.query(User).all()
        return {"status": "success", 
                "users": [
                    {"id": user.id, 
                     "name": user.name, 
                     "password": user.password} 
                    for user in users
                    ]}   