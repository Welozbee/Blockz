from pydantic import BaseModel, Field, model_validator, ConfigDict

import bdd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


# Connexion à la base de données + Tout préparer
conn = bdd.get_connection()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Block(BaseModel):
    model_config = ConfigDict(extra="forbid")  # optionnel: refuse les champs inconnus

    id: int = Field(ge=0)
    name: str = Field(min_length=1)
    displayName: str = Field(min_length=1)
    hardness: float = Field(ge=-1)
    resistance: float = Field(ge=0)
    stackSize: int = Field(ge=1, le=64)
    diggable: bool
    material: str = Field(min_length=1)
    transparent: bool
    emitLight: int = Field(ge=0, le=15)

    @model_validator(mode="after")
    def validate_consistency(self) -> "Block":
        # Règle: un bloc diggable ne peut pas être incassable
        if self.diggable and self.hardness == -1:
            raise ValueError("Invalid block: diggable=True but hardness=-1 (unbreakable).")
        return self

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
            raise HTTPException(status_code=404, detail="Block not found")

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

# Router pour modifier un bloc existant
@app.put("/block/{id}", response_model=Block)
async def modify_block(id: int, block: Block):
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM blocks WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Block not found")

    validated_block = Block(
        id=id,
        **block.model_dump(exclude={"id"})
    )

    cursor.execute(
        """
        UPDATE blocks
        SET name = ?,
            displayName = ?,
            hardness = ?,
            resistance = ?,
            stackSize = ?,
            diggable = ?,
            material = ?,
            transparent = ?,
            emitLight = ?
        WHERE id = ?
        """,
        (
            validated_block.name,
            validated_block.displayName,
            validated_block.hardness,
            validated_block.resistance,
            validated_block.stackSize,
            int(validated_block.diggable),
            validated_block.material,
            int(validated_block.transparent),
            validated_block.emitLight,
            id,
        ),
    )
    conn.commit()

    return validated_block

from fastapi import Body, HTTPException
from pydantic import ValidationError

@app.post("/block", response_model=Block, status_code=201)
async def create_block(payload: Block = Body(...)):
    cursor = conn.cursor()

    validated = Block(
        id=0,  # id temporaire juste pour satisfaire le modèle
        **payload.model_dump(exclude={"id"})
    )

    cursor.execute(
        """
        INSERT INTO blocks
            (name, displayName, hardness, resistance, stackSize, diggable, material, transparent, emitLight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            validated.name,
            validated.displayName,
            validated.hardness,
            validated.resistance,
            validated.stackSize,
            int(validated.diggable),
            validated.material,
            int(validated.transparent),
            validated.emitLight,
        ),
    )
    conn.commit()

    new_id = cursor.lastrowid

    # 3) Retourner l'objet final (re-validé, cette fois avec le vrai id)
    return Block(id=new_id, **validated.model_dump(exclude={"id"}))


