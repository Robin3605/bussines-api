from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.config.db import init_db
from src.routes import users, auth, products, cart
from src.helpers.api_responses import APIResponses
from src.config.cloudinary import cloudinary


app = FastAPI(title="Bussiness API")

@app.on_event("startup")
async def start_db():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

@app.exception_handler(APIResponses)
async def api_error_handler(request: Request, exc: APIResponses):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "status_text": APIResponses.switch.get(exc.status_code, "Unknown"),
            "path": request.url.path,
        },
    )

# create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://niborai.vercel.app",],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"], 
)

app.include_router(users.router) # aca es donde se agregan la rutas
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)