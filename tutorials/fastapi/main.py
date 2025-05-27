from fastapi import FastAPI, HTTPException
from models import Todo

## LINKS:
## https://latenode.com/blog/http-request-methods#:~:text=It's%20essential%20to%20grasp%20this,a%20POST%20or%20PUT%20request.
## https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/PATCH


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

todos = []

## Create TODO
@app.post("/todos")
async def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo has been added", "http_code": 201}

## Get all TODO
@app.get("/todos")
async def get_todos():
    return {"todos": todos, "http_code": 200}

## Get single TODO
@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return {"todo": todo, "http_code":200}
    
    raise HTTPException(status_code=404, detail=f"No todo with id {todo_id} exists")


## Delete a TODO
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": f"Todo with id {todo_id} has been deleted", "http_code":200}
    
    raise HTTPException(status_code=404, detail=f"No todo with id {todo_id} exists")

## Update TODO
## PUT request creates a new resource if it does not exist or completely replaces it
@app.put("/todos/{todo_index}")
async def update_todo(todo_index: int, todo_obj: Todo):
    if todo_index < len(todos):
        todos[todo_index] = todo_obj
        return {"message": f"Successfully updated todo at index {todo_index}", "http_code": 200}

    else:
        raise HTTPException(status_code=404, detail=f"No todo at index {todo_index} exists")

## PATCH request updates only a portion of existing resource
@app.patch("/todos")
async def update_todo(todo_obj: Todo):
    todo_id = todo_obj.id
    for todo in todos:
        if todo.id == todo_id:
            todo.item = todo_obj.item ## Updating portion of existing resource here!
            return {"message": "Successfully updated todo with id {todo_id}", "http_code": 200}
    
    raise HTTPException(status_code=404, detail=f"No todo with id {todo_id} exists")



