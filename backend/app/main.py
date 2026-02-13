from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ganzhi, nayin, shensha, guanxi, admin

app = FastAPI(
    title="六十甲子象意百科查询系统 API",
    description="提供干支基础信息、纳音五行、神煞、象意、喜忌、干支关系等知识的API",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Register routers
app.include_router(ganzhi.router)
app.include_router(nayin.router)
app.include_router(shensha.router)
app.include_router(guanxi.router)
app.include_router(admin.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "六十甲子象意百科查询系统 API", "version": "1.0.0"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
