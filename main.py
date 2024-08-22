from fastapi import FastAPI, Request, Response, File, UploadFile, Query

from controllers.o365 import login_o365 , auth_callback_o365
from controllers.google import login_google , auth_callback_google
from controllers.firebase import register_user_firebase, login_user_firebase, generate_activation_code, activate_user
from controllers.edificios import fetch_edificios, fetch_aulas
from controllers.clases import fetch_clases, fetch_carreras, fetch_facultades, fetch_clase
from controllers.extras import fetch_docentes, fetch_terms
from controllers.secciones import fetch_secciones_aula, fetch_seccion_carrera, fetch_secciones_carrera, update_seccion, delete_seccion, create_seccion

from models.UserRegister import UserRegister
from models.UserLogin import UserLogin
from models.UserActivation import UserActivation
from models.seccion import seccion

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



""" Login """
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
async def login_custom(user: UserLogin):
    return await login_user_firebase(user)




@app.get("/user")
@validate
async def user(request: Request):
    return {
        "email": request.state.email
    }

@app.get("/terms")
@validate
async def terms(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_terms( )

@app.get("/docentes/{id}")
@validate
async def docentes(request: Request, response: Response, id: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_docentes(id)



""" Edificios """
@app.get("/edificios")
@validate
async def edificio(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_edificios( )

@app.get("/edificios/{id}")
@validate
async def edificio(request: Request, response: Response, id: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_aulas(id)

@app.get("/edificios/{id_edificio}/aulas/{id_aula}/term/{term}")
@validate
async def edificio(request: Request, response: Response, id_edificio: str, id_aula: int, term: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_secciones_aula(id_edificio, id_aula, term)



""" Facultades """
@app.get("/facultades")
@validate
async def clase(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_facultades()

@app.get("/facultades/{id}")
@validate
async def clase(request: Request, response: Response, id: int):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_carreras(id)

@app.get("/facultades/{id_facultad}/carrera/{id_carrera}/term/{term}")
@validate
async def clase(request: Request, response: Response, id_facultad: int, id_carrera: str, term: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_clases( id_carrera, term)



""" Secciones """
@app.get("/facultades/{id_facultad}/carrera/{id_carrera}/clase/{id_clase}/term/{term}/secciones")
@validate
async def clase(request: Request, response: Response, id_facultad: int, id_carrera: str, id_clase: int, term: str):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_secciones_carrera(id_carrera, id_clase, term)

@app.get("/term/{id_term}/carrera/{id_carrera}/clase/{id_clase}")
@validate
async def clase(request: Request, response: Response, id_term: str, id_carrera: str, id_clase: int):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_clase(id_carrera, id_clase)

@app.get("/facultades/{id_facultad}/carrera/{id_carrera}/clase/{id_clase}")
@validate
async def clase(request: Request, response: Response, id_facultad: int, id_carrera: str, id_clase: int):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_clase(id_carrera, id_clase)

@app.get("/term/{id_term}/carrera/{id_carrera}/clase/{id_clase}/seccion/{id_seccion}")
@validate
async def clase(request: Request, response: Response, id_term: str, id_seccion: int, id_carrera: str, id_clase: int):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_seccion_carrera(id_term, id_carrera, id_clase, id_seccion)

@app.put("/term/{id_term}/carrera/{id_carrera}/clase/{id_clase}/seccion/{id_seccion}")
@validate
async def actualizar_seccion(request: Request, response: Response, id_term: str, id_carrera: str, id_clase: int, id_seccion: int, section: seccion):
    response.headers["Cache-Control"] = "no-cache"
    return await update_seccion(id_term, id_carrera, id_clase, id_seccion, section.Cod_Edificio, section.Num_Aula, section.Num_Empleado, section.Cupos, section.Dias, section.Hora_Inicial, section.Hora_Final, section.Portada)

@app.delete("/term/{id_term}/carrera/{id_carrera}/clase/{id_clase}/seccion/{id_seccion}")
@validate
async def borrar_seccion(request: Request, response: Response, id_term: str, id_carrera: str, id_clase: int, id_seccion: int):
    response.headers["Cache-Control"] = "no-cache"
    return await delete_seccion(id_term, id_carrera, id_clase, id_seccion)

@app.post("/seccion")
@validate
async def crear_seccion(request: Request, response: Response, section: seccion):
    response.headers["Cache-Control"] = "no-cache"
    return await create_seccion(section)


""" BLOB STORAGE """
@app.post("/user/{id}/profile")
@validate
async def upload_files(request: Request, response: Response, id: int, files: list[UploadFile] = File(...) ):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_upload_profile( request.state.email, id, files )

@app.get("/user/{id}/profile")
@validate
async def download_files(request: Request, response: Response, id: int):
    response.headers["Cache-Control"] = "no-cache"
    return await fetch_profile(id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)