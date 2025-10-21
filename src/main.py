from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# @app.on_event("startup")
# async def on_startup():
#     with next(get_db()) as session:
#         seed_subscription_plans(session)
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

# @app.exception_handler(APIResponses)
# async def api_error_handler(request: Request, exc: APIResponses):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "message": exc.message,
#             "status_text": APIResponses.switch.get(exc.status_code, "Unknown"),
#             "path": request.url.path,
#         },
#     )

# create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://niborai.vercel.app",],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"], 
)

# app.include_router(users.router) # aca es donde se agregan la rutas