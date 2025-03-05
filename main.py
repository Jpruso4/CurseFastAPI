from fastapi import FastAPI, Body, Path, Query, status

from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import List

from jwt_config import create_token

# Create instance FastAPI 
app = FastAPI()
app.title = "Sales Aplication"
app.version = "1.0.1"

# List of Sales Examples
salesList = [
    {
        "id":1,
        "date":"01/01/25",
        "store":"Walmart",
        "amount":10
    },
    {
        "id":2,
        "date":"02/02/25",
        "store":"Target",
        "amount":20,
    },
    {
        "id":4,
        "date":"02/02/25",
        "store":"Target",
        "amount":30,
    },
    {
        "id":3,
        "date":"03/03/25",
        "store":"Publix",
        "amount":30
    }
]

#Create Model Sales
class Sales(BaseModel):
    id: int = Field(ge=0, le=50)
    date: str
    store: str = Field(min_length=4, max_length=20)
    amount: float
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "date": "01/01/99",
                "store": "Example01",
                "amount": 123.0
            }
        }
    )
    
# Create Model User
class User(BaseModel):
    email:str
    password:str


# Endpoints of Sales
@app.get('/', tags=["Home"]) # Cambio de etiqueta en la documentación
def message():
    return HTMLResponse("<h2>Titule HTML from FastAPI<h2>")



@app.get("/sales", tags=["Sales"], response_model = List[Sales], status_code = status.HTTP_200_OK)
def sales() -> List[Sales]:
    return JSONResponse(content=salesList, status_code = status.HTTP_200_OK)



@app.get("/sales/{id}", tags=["Sales"], response_model = Sales, status_code = status.HTTP_200_OK)
def sale(id:int = Path(ge=1,le=1000)) -> Sales:
    for saleItem in salesList:
        print(salesList)
        if saleItem["id"] == id:
            return JSONResponse(content=saleItem, status_code = status.HTTP_200_OK)
    return JSONResponse(content=[], status_code = status.HTTP_404_NOT_FOUND)


    
@app.get("/sales/", tags=["Sales"], response_model = List[Sales], status_code = status.HTTP_200_OK)
def store_sales(store:str = Query(min_length=4, max_length=20)) -> List[Sales]:
    dataList = [saleItem for saleItem in salesList if saleItem["store"] == store]
    return JSONResponse(content=dataList, status_code = status.HTTP_200_OK)



@app.post("/createSale", tags=["Sales"], response_model = dict, status_code = status.HTTP_201_CREATED)
def create_sale(sale: Sales = Body(...)) -> dict:
    salesList.append(sale.model_dump())
    return JSONResponse(content={"message": "Created Sale Successfull"}, status_code = status.HTTP_201_CREATED)




@app.put("/modifiedSale/{id}", tags=["Sales"], response_model = dict, status_code = status.HTTP_201_CREATED)
def modified_sale(id:int, sale:Sales) -> dict:
    for saleItem in salesList:
        if saleItem["id"] == id:
            saleItem["date"] = sale.date
            saleItem["store"] = sale.store
            saleItem["amount"] = sale.amount
    return JSONResponse(content={"message": "Modified Sale Successfull"}, status_code = status.HTTP_201_CREATED)



@app.delete("/deleteSale/{id}", tags=["Sales"], response_model = dict, status_code = status.HTTP_200_OK)
def delete_sale(id:int) -> dict:
    for saleItem in salesList:
        if saleItem["id"] == id:
            salesList.remove(saleItem)
    return JSONResponse(content={"message": "Deleted Sale Successfull"}, status_code = status.HTTP_200_OK)


# Create Endpoint to Login
@app.post("/login", tags=["Autenticate"])
def login_user(user:User):
    if user.email == "juan@gmail.com" and user.password == "1234":
        token:str = create_token(user.model_dump())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)
    else:
        return JSONResponse(content={"message": "Denied Access"}, status_code = status.HTTP_404_NOT_FOUND)
