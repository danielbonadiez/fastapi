from connection.conexion import connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel



app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    
# CRUD Operations
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO items (name, description, price) VALUES (%s, %s, %s)", (item.name, item.description, item.price))
        connection.commit()
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, name, description, price FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        return Item(id=item[0], name=item[1], description=item[2], price=item[3])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE items SET name = %s, description = %s, price = %s WHERE id = %s", (item.name, item.description, item.price, item_id))
        connection.commit()
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        connection.commit()
        return {"message": "Item deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
