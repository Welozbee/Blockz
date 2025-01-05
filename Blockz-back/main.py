from pydantic import BaseModel

import bdd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

# Connexion à la base de données + Tout préparer
conn = bdd.get_connection()
app = FastAPI()

class Block(BaseModel):
    id: int
    name: str
    displayName: str
    hardness: float
    resistance: float
    stackSize: int
    diggable: bool
    material: str
    transparent: bool
    emitLight: int

# Route pour récupérer tous les blocs
@app.get("/blocks",response_model=List[Block])
async def get_blocks():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blocks")
        result = cursor.fetchall()
        blocks = [
            Block(
                id=row[0],
                name=row[1],
                displayName=row[2],
                hardness=row[3],
                resistance=row[4],
                stackSize=row[5],
                diggable=bool(row[6]),
                material=row[7],
                transparent=bool(row[8]),
                emitLight=row[9],
            )
            for row in result
        ]
        return blocks


# Route pour récupérer un bloc par ID
@app.get("/block/{id}",response_model=Block)
async def get_block(id: int):
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM blocks WHERE id = {id}")
        row = cursor.fetchone()

        if row is None:
            return JSONResponse(content={"error": "Block not found"}, status_code=404)

        block = Block(
            id=row[0],
            name=row[1],
            displayName=row[2],
            hardness=row[3],
            resistance=row[4],
            stackSize=row[5],
            diggable=bool(row[6]),
            material=row[7],
            transparent=bool(row[8]),
            emitLight=row[9],
        )
        return block