from models.user import UpdateUser ,Login,User,UserResponse,DeleteResponse
from database import get_connection
from utils.hash import hash_password , verify_password
from typing import List
import mysql.connector as ms 
from fastapi import APIRouter , HTTPException ,Depends
from utils.jwt import create_access_token ,verify_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # الرابط الخاص بالـ login endpoint

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

router=APIRouter()
@router.get("/users/",response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_user)):
    try:
        conn=get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT id,name,age,email FROM users")
        all_users=cursor.fetchall()
        return all_users
    except ms.Error as e:
        raise HTTPException(status_code=500,detail=f"My SQL Error{str(e)}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()    

@router.get("/users/{user_id}",response_model=UserResponse)
async def get_user(user_id:int , current_user: dict = Depends(get_current_user)):
    try:
        conn=get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT id,name,age,email FROM users WHERE id =%s",(user_id,))
        fetch=cursor.fetchone()
        if fetch is None:
            raise HTTPException(status_code=404,detail="user not found")
        return fetch
    except ms.Error as e:
        raise HTTPException(status_code=500,detail=f"My SQL Error{str(e)}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()    

@router.post("/users/",response_model=UserResponse)
async def add_users(user:User):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        password_hash=hash_password(user.password)
        cursor.execute("INSERT INTO users (name,age,Email,password_hash) VALUES(%s,%s,%s,%s)",(user.name,user.age,user.email,password_hash,))
        conn.commit()
        user_id=cursor.lastrowid
        return UserResponse(
            id=user_id,
            name=user.name,
            age=user.age,
            email=user.email,

        )
    except ms.Error as e:
        raise HTTPException(status_code=500,detail=f"My SQL Error{str(e)}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()    

@router.put("/users/{user_id}",response_model=UserResponse)
async def update_users(user_id:int , update_user:UpdateUser ,current_user: dict = Depends(get_current_user)):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        if user_id != current_user["user_id"]:
         raise HTTPException(status_code=403, detail="Not authorized")
        cursor.execute("UPDATE users SET name=%s , age=%s , email=%s WHERE id =%s",(update_user.name,update_user.age,update_user.email,user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException (status_code=404,detail="user not found")
        return UserResponse(
            id=user_id,
            name=update_user.name,
            age=update_user.age,
            email=update_user.email
        )
    except ms.Error as e:
        raise HTTPException(status_code=500,detail=f"My SQL Error{str(e)}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()    


@router.delete("/users/{user_id}",response_model=DeleteResponse)
async def delete_users(user_id:int,current_user: dict = Depends(get_current_user)):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        if user_id != current_user["user_id"]:
         raise HTTPException(status_code=403, detail="Not authorized")

        cursor.execute("DELETE FROM users WHERE id =%s",(user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404,detail="user not found")
       
        return DeleteResponse(
            message="deleted",
            user_id=user_id
        )
    except ms.Error as e:
        raise HTTPException(status_code=500,detail=f"My SQL Error{str(e)}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()    

@router.post("/login/")
async def login(login: Login):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Email = %s", (login.email,))
        user = cursor.fetchone()
        if user is None or not verify_password(login.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="wrong email or password")

        # إنشاء JWT token
        access_token = create_access_token({"user_id": user["id"], "email": user["Email"]})
        return {"access_token": access_token, "token_type": "bearer"}

    except ms.Error as e:
        raise HTTPException(status_code=500, detail=f"MySQL Error: {str(e)}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()