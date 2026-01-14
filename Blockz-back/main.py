import base64
import hashlib
import hmac
import json
import os
import sqlite3
import time
from typing import List, Optional
from uuid import uuid4

import bdd
from fastapi import Body, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, model_validator


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "blocks")
MAX_IMAGE_BYTES = 2_000_000

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Connexion à la base de données + Tout préparer
conn = bdd.get_connection()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    if bdd.ENV == "DEV":
        JWT_SECRET = "dev-secret"
        print("JWT_SECRET manquant, valeur par defaut utilisee en DEV.")
    else:
        raise RuntimeError("JWT_SECRET manquant.")

JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "uploads")), name="static")
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
    imagePath: Optional[str] = None

    @model_validator(mode="after")
    def validate_consistency(self) -> "Block":
        # Règle: un bloc diggable ne peut pas être incassable
        if self.diggable and self.hardness == -1:
            raise ValueError("Invalid block: diggable=True but hardness=-1 (unbreakable).")
        return self


def _row_to_block(row, image_path_override: Optional[str] = None) -> Block:
    return Block(
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
        imagePath=image_path_override if image_path_override is not None else row[10],
    )


class AuthRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class MeResponse(BaseModel):
    username: str
    role: str


def _placeholder() -> str:
    return "?" if isinstance(conn, sqlite3.Connection) else "%s"


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    iterations = 200_000
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2_sha256${}${}${}".format(
        iterations,
        base64.urlsafe_b64encode(salt).decode("ascii").rstrip("="),
        base64.urlsafe_b64encode(hashed).decode("ascii").rstrip("="),
    )


def _verify_password(password: str, stored: str) -> bool:
    try:
        algo, iterations, salt_b64, hash_b64 = stored.split("$", 3)
        if algo != "pbkdf2_sha256":
            return False
        salt = _b64url_decode(salt_b64)
        expected = _b64url_decode(hash_b64)
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(hashed, expected)
    except Exception:
        return False


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def _encode_jwt(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def _decode_jwt(token: str) -> dict:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected = hmac.new(JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(_b64url_decode(signature_b64), expected):
            raise HTTPException(status_code=401, detail="Token invalide.")
        payload = json.loads(_b64url_decode(payload_b64))
    except ValueError:
        raise HTTPException(status_code=401, detail="Token invalide.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=401, detail="Token invalide.")

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        raise HTTPException(status_code=401, detail="Token expire.")
    return payload


def _ensure_admin_user() -> None:
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        print("ADMIN_USERNAME ou ADMIN_PASSWORD manquant, admin non cree.")
        return

    cursor = conn.cursor()
    ph = _placeholder()
    cursor.execute(f"SELECT id FROM users WHERE username = {ph}", (username,))
    if cursor.fetchone() is None:
        password_hash = _hash_password(password)
        cursor.execute(
            f"INSERT INTO users (username, password_hash, role) VALUES ({ph}, {ph}, {ph})",
            (username, password_hash, "admin"),
        )
        conn.commit()


def _get_current_user(authorization: Optional[str]) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization manquante.")
    token = authorization.split(" ", 1)[1].strip()
    return _decode_jwt(token)

def _require_admin(authorization: Optional[str]) -> dict:
    user = _get_current_user(authorization)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acces refuse.")
    return user


_ensure_admin_user()

# Route pour récupérer tous les blocs
@app.get("/blocks",response_model=List[Block])
async def get_blocks():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blocks")
        result = cursor.fetchall()
        blocks = [
            _row_to_block(row)
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

        block = _row_to_block(row)
        return block

# Router pour modifier un bloc existant
@app.put("/block/{id}", response_model=Block)
async def modify_block(id: int, block: Block, authorization: Optional[str] = Header(default=None)):
    _require_admin(authorization)
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
            emitLight = ?,
            image_path = ?
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
            validated_block.imagePath,
            id,
        ),
    )
    conn.commit()

    return validated_block

@app.post("/block", response_model=Block, status_code=201)
async def create_block(payload: Block = Body(...), authorization: Optional[str] = Header(default=None)):
    _require_admin(authorization)
    cursor = conn.cursor()

    validated = Block(
        id=0,  # id temporaire juste pour satisfaire le modèle
        **payload.model_dump(exclude={"id"})
    )

    cursor.execute(
        """
        INSERT INTO blocks
            (name, displayName, hardness, resistance, stackSize, diggable, material, transparent, emitLight, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            validated.imagePath,
        ),
    )
    conn.commit()

    new_id = cursor.lastrowid

    # 3) Retourner l'objet final (re-validé, cette fois avec le vrai id)
    return Block(id=new_id, **validated.model_dump(exclude={"id"}))


@app.post("/block/{id}/image", response_model=Block)
async def upload_block_image(
    id: int,
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(authorization)
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Type de fichier invalide.")

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise HTTPException(status_code=400, detail="Extension invalide.")

    content = await file.read()
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux.")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blocks WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Block not found")

    filename = f"{id}_{uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, filename)
    with open(dest_path, "wb") as dest:
        dest.write(content)

    image_path = f"blocks/{filename}"
    cursor.execute("UPDATE blocks SET image_path = ? WHERE id = ?", (image_path, id))
    conn.commit()

    return _row_to_block(row, image_path_override=image_path)


@app.post("/auth/login", response_model=AuthResponse)
async def login(payload: AuthRequest):
    cursor = conn.cursor()
    ph = _placeholder()
    cursor.execute(
        f"SELECT username, password_hash, role FROM users WHERE username = {ph}",
        (payload.username,),
    )
    row = cursor.fetchone()
    if row is None or not _verify_password(payload.password, row[1]):
        raise HTTPException(status_code=401, detail="Identifiants invalides.")

    exp = int(time.time()) + (JWT_EXPIRES_MINUTES * 60)
    token = _encode_jwt({"sub": row[0], "role": row[2], "exp": exp})
    return AuthResponse(access_token=token, role=row[2])


@app.get("/me", response_model=MeResponse)
async def me(authorization: Optional[str] = Header(default=None)):
    user = _get_current_user(authorization)
    return MeResponse(username=user["sub"], role=user["role"])
