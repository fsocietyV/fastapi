import sqlite3
from sqlmodel import Field, SQLModel, select, create_engine, Session
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

conn = sqlite3.connect(r"Tester.db", check_same_thread=False)
app = FastAPI()



templates = Jinja2Templates(directory="templates")

@app.post("/names")
def fetch_data(Name: str, Surname: str, Sub_status: str):
    insert_query = f"INSERT INTO Customer(Name, Surname, Sub_status) VALUES({Name}, {Surname}, {Sub_status})"
    cursor = conn.execute(insert_query)
    results = conn.commit()

#@app.post("/users_post")
#async def fetch_data(User_ID: int, Login: str, Sub_stat: int, Subscription_up: str):
#    insert_query = f"INSERT INTO  ACCOUNTS(User_ID, Login, Sub_stat, Subscription_up) VALUES({User_ID}, {Login}, {Sub_stat}, {Subscription_up})"
#    cursor = conn.execute(insert_query)
#    results = conn.commit()

@app.get("/")
def info(request: Request):
    coursor = str("Hi, there are a couple of sections here, add to the address link: '/logins, /names or /status")
    return templates.TemplateResponse("hello.html", {"coursor": coursor, "request": request})

@app.get("/logins")
def get_users(request: Request):
    cursor = conn.execute("SELECT * FROM Accounts;")
    result = [
        {
            "id": user[0], "Login": user[1], "Subscription status": user[2], "subscription up": user[3]
        } for user in cursor.fetchall()
    ]
    return templates.TemplateResponse("users.html", {"result": result, "request": request})

@app.get("/names")
def get_names(request: Request):
    cursor = conn.execute("SELECT * FROM Customer;")
    result = [
        {
            "id": user[0], "name": user[1], "surname": user[2], "sub_st": user[3]
        } for user in cursor.fetchall()
    ]
    return templates.TemplateResponse("names.html", {"result": result, "request": request})


@app.patch("/names/{id}", status_code=status.HTTP_200_OK)
def update_user(id: int, name: str, surname: str, sub_status: str):
    cursor = conn.execute(f"SELECT * FROM customer WHERE customer.id={id};")
    query_result = cursor.fetchone()
    if not query_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    conn.execute(f"UPDATE customer SET name = ('{name}'), surname = ('{surname}'), sub_status = ('{sub_status}') WHERE id={id}")
    conn.commit()

@app.delete("/names/{id}")
def delete_user(id: int):
    cursor = conn.execute(f"SELECT * FROM Customer WHERE Customer.id={id};")
    user = cursor.fetchone()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    conn.execute(f"DELETE FROM Customer WHERE id={id}")

@app.get("/status")
def get_list_of_status(request: Request):
    cursor = conn.execute("SELECT * FROM Status;")
    result = [
        {
            "id": user[0], "Status": user[1]
        } for user in cursor.fetchall()
    ]
    return templates.TemplateResponse("status.html", {"result": result, "request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
