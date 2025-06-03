from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import init_db
from app.models.model import Libro
from app.schemas import LibroResponse, LibroCreate
from app.schemas import LibroCreate
from fastapi import Query, HTTPException
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.on_event("startup")
async def startup():
    await init_db()


@app.post("/libros", response_model=LibroResponse, status_code = 201)   # Crear un nuevo libro
async def crear_libro(libro: LibroCreate):
    existente = await Libro.filter(isbn = libro.isbn).first()
    if existente:
        raise HTTPException(status_code = 400, detail = "Esta isbn de libro ya está en uso") 
    nuevo_libro = await Libro.create(**libro.dict())
    return nuevo_libro

@app.get("/libros", response_model = list[LibroResponse])  # Listar todos los libros
async def listar_libros():
    return await Libro.all()

@app.get("/libros/{id}", response_model=LibroResponse)  # Obtener un libro específico filtrando con id
async def obtener_libro(id: int):
    libro = await Libro.get_or_none(id=id)
    if not libro:
        raise HTTPException(status_code = 404, detail = "Libro no encontrado")
    return libro


@app.get("/libros/buscar/{str_titulo}", response_model=LibroResponse)  # Obtener un libro específico filtr
async def obtener_libro(str_titulo: str):
    libro = await Libro.get_or_none(titulo=str_titulo)
    if not libro:
        raise HTTPException(status_code = 404, detail = "Libro no encontrado")
    return libro


@app.put("/libros/{id}", response_model=LibroResponse)   # Actualizar un libro, usa la id para identificar cuál quiere actualizar
async def actualizar_libro(id: int, libro: LibroCreate):
    await Libro.filter(id=id).update(**libro.dict(exclude_unset=True))
    return await Libro.get(id=id)

@app.delete("/libros/{id}")  # Eliminar un libro, usa la id para identificar cuál quiere eliminar
async def eliminar_libro(id: int):
    deleted_count = await Libro.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail = "Libro no encontrado")
    return {"message": "Libro eliminado"}