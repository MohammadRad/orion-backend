from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import User, Project, Task, TaskStatus
from .schemas import (
    UserCreate, UserOut, TokenOut,
    ProjectCreate, ProjectOut,
    TaskCreate, TaskOut,
)
from .auth import hash_password, verify_password, create_access_token, decode_access_token

app = FastAPI(title="orion-backend")
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        uid = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.get(User, uid)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/health")
def health():
    return {"status": "ok"}

# --- Auth ---
@app.post("/auth/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email exists")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@app.post("/auth/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    return TokenOut(access_token=create_access_token(str(user.id)))

# --- Projects ---
@app.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = Project(name=data.name, description=data.description, owner_id=user.id)
    db.add(project); db.commit(); db.refresh(project)
    return project

@app.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Project).filter(Project.owner_id == user.id).all()

# --- Tasks ---
@app.post("/tasks/{project_id}", response_model=TaskOut, status_code=201)
def create_task(project_id: int, data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.get(Project, project_id)
    if not project or project.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task(title=data.title, status=data.status, project_id=project_id)
    db.add(task); db.commit(); db.refresh(task)
    return task
