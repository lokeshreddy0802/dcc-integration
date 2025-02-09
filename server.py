from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import time

app = FastAPI()

# SQLite Database Setup
conn = sqlite3.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS inventory (name TEXT, quantity INTEGER)")
conn.commit()

# Define Data Models for Validation
class TransformData(BaseModel):
    name: str
    location: list[float] = []
    rotation: list[float] = []
    scale: list[float] = []

class TranslationData(BaseModel):
    name: str
    location: list[float]

class RotationData(BaseModel):
    name: str
    rotation: list[float]

class ScaleData(BaseModel):
    name: str
    scale: list[float]

#  **1. Handle Full Transform Data (Position, Rotation, Scale)**
@app.post("/transform")
async def transform(data: TransformData):
    try:
        time.sleep(10)  # Simulate delay
        return {"status": "success", "data": data.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **2. Handle Only Position (Translation)**
@app.post("/translation")
async def translation(data: TranslationData):
    try:
        return {"status": "success", "location": data.location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **3. Handle Only Rotation**
@app.post("/rotation")
async def rotation(data: RotationData):
    try:
        return {"status": "success", "rotation": data.rotation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **4. Handle Only Scale**
@app.post("/scale")
async def scale(data: ScaleData):
    try:
        return {"status": "success", "scale": data.scale}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **5. Return File Path (Optional: Project Path)**
@app.get("/file-path")
async def file_path(projectpath: bool = False):
    try:
        if projectpath:
            return {"project_path": "/home/lokesh/Desktop/my_project.blend"}
        return {"file_path": "/home/lokesh/Desktop/my_project.blend/untitled.blend"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **6. Add Item to Inventory**
@app.post("/add-item")
async def add_item(name: str, quantity: int):
    try:
        cursor.execute("INSERT INTO inventory VALUES (?, ?)", (name, quantity))
        conn.commit()
        return {"status": "Item added"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **7. Remove Item from Inventory**
@app.post("/remove-item")
async def remove_item(name: str):
    try:
        cursor.execute("DELETE FROM inventory WHERE name = ?", (name,))
        conn.commit()
        return {"status": "Item removed"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **8. Update Quantity of an Existing Item (FIXED RESPONSE FORMAT)**
@app.post("/update-quantity")
async def update_quantity(name: str, new_quantity: int):
    try:
        cursor.execute("UPDATE inventory SET quantity = ? WHERE name = ?", (new_quantity, name))
        conn.commit()
        return {"status": "Item quantity updated"}  # 🔹 FIXED RESPONSE
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

#  **Run the Server**
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

