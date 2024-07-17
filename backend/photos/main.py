import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core import settings
from api.api_v1.api import api_router



# @app.middleware("http")
# async def session_db(request: Request, call_next):
#     async with AsyncSession(bind=engine, expire_on_commit=False) as session:
#         request.state.db = Database(session)
#         response = await call_next(request)
#     return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    yield
    print("server is stopping")

app = FastAPI(openapi_url=f"/{settings.api.CURRENT_VERSION}/openapi.json",
              lifespan=lifespan,

              )


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/"+settings.api.CURRENT_VERSION)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.run.HOST, port=settings.run.PORT)