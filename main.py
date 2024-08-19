from fastapi import FastAPI, Request, Response, File, UploadFile, Query

from controllers.o365 import login_o365 , auth_callback_o365
from controllers.google import login_google , auth_callback_google
from controllers.firebase import register_user_firebase, login_user_firebase, generate_activation_code, activate_user
from controllers.edificios import fetch_edificios, fetch_aulas
from controllers.clases import fetch_clases, fetch_carreras, fetch_facultades
from controllers.extras import fetch_docentes, fetch_terms
from controllers.secciones import fetch_secciones_aula, fetch_seccion_carrera, fetch_secciones_carrera, update_seccion, delete_seccion

from models.UserRegister import UserRegister
from models.UserLogin import UserLogin
from models.UserActivation import UserActivation
from models.clase import clase

from fastapi.middleware.cors import CORSMiddleware
from utils.security import validate, validate_func, validate_for_inactive

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
async def hello():
    return {
        "Hello": "World"
        , "version": "0.1.0"
    }

@app.get("/login/m365")
async def login():
    return await login_o365()

@app.get("/auth/m365/callback")
async def authcallback(request: Request):
    return await auth_callback_o365(request)

@app.get("/login/google")
async def logingoogle():
    return await login_google()

@app.get("/auth/google/callback")
async def authcallbackgoogle(request: Request):
    return await auth_callback_google(request)

@app.post("/register")
async def register(user: UserRegister):
    return await register_user_firebase(user)


@app.post("/login/custom")
async def login_custom(user: UserRegister):
    return await login_user_firebase(user)


@app.get("/user")
@validate
async def user(request: Request):
    return {
        "email": request.state.email
    }

@app.get("/terms")
async def terms(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_terms( )

@app.get("/docentes/{id}")
async def docentes(request: Request, response: Response, id: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_docentes(id)

@app.get("/edificios")
async def edificio(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_edificios( )

@app.get("/edificios/{id}")
async def edificio(request: Request, response: Response, id: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_aulas(id)

@app.get("/edificios/{id_edificio}/aulas/{id_aula}/term/{term}")
async def edificio(request: Request, response: Response, id_edificio: str, id_aula: int, term: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_secciones_aula(id_edificio, id_aula, term)

@app.get("/facultades")
async def clase(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_facultades()

@app.get("/facultades/{id}")
async def clase(request: Request, response: Response, id: int):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_carreras(id)

@app.get("/facultades/{id_facultad}/carrera/{id_carrera}/term/{term}")
async def clase(request: Request, response: Response, id_facultad: int, id_carrera: str, term: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_clases( id_carrera, term)

@app.get("/facultades/{id_facultad}/carrera/{id_carrera}/clase/{id_clase}/term/{term}")
async def clase(request: Request, response: Response, id_facultad: int, id_carrera: str, id_clase: int, term: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_secciones_carrera(id_carrera, id_clase, term)

@app.get("/facultades/{id_facultad}/carrera/{id_carrera}/clase/{id_clase}/seccion/{id_seccion}")
async def clase(request: Request, response: Response, id_seccion: int, id_carrera: str, id_clase: int, id_facultad: int):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_seccion_carrera(id_carrera, id_clase, id_seccion)

@app.put("/facultades/{id_facultad}/carrera/{id_carrera}/clase/{id_clase}/seccion/{id_seccion}")
async def clase(request: Request, response: Response, id_seccion: int, id_carrera: str, id_clase: int, id_facultad: int):
    response.headers["Cache-Control"] = "no-cache"
    return await update_seccion(id_carrera, id_clase, id_seccion)

@app.delete("/facultades/{id_facultad}/carrera/{id_carrera}/clase/{id_clase}/seccion/{id_seccion}")
async def clase(request: Request, response: Response, id_seccion: int, id_carrera: str, id_clase: int, id_facultad: int):
    response.headers["Cache-Control"] = "no-cache"
    return await delete_seccion(id_carrera, id_clase, id_seccion)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)