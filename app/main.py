from fastapi import FastAPI
from app.api.v1.routes import auth, user,course, enrollment
from app.core.config import settings

app = FastAPI(title="Course Enrollment Platform")
app.include_router(auth.router, prefix=f'{settings.API_V1_STR}/auth', tags=["Auth"])
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/user", tags=["User"])
app.include_router(course.router, prefix=f"{settings.API_V1_STR}/course", tags=["Course"])
app.include_router(enrollment.router, prefix=f"{settings.API_V1_STR}/enrollment", tags=["Enrollment"])

@app.get("/")
def root():
    return {
        "message":"Welcom to Course Enrollemet Platform"
    }