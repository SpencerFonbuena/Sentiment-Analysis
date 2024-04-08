from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import general_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware


app = FastAPI()
app.include_router(general_router)
# Add Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers = ['*']
)

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})

@app.post('/cors-test')
def health_check():
    return JSONResponse(content={"status": "good test!"})