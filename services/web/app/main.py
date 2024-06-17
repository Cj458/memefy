from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.web.routes.meme_routes import router as meme_router
# from common.responses.custom_exceptions_handler import custom_exception_handler
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI(
    docs_url="/api/meme/docs",
    redoc_url="/api/meme/redoc",
    openapi_url="/api/meme/openapi.json"
)
# app.include_router(guest_router)
app.include_router(meme_router)

# add custom exception handler
# app.add_exception_handler(RequestValidationError, custom_exception_handler)
# add auth middleware


origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)

#

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})

