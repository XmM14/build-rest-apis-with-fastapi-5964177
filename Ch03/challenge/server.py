"""
Write an HTTP server that will accept requests to start a virtual machine (VM) and to
shut it down.

Start:

    POST http://localhost:8000/vm/start

    {
        "cpu_count": 2,
        "mem_size_gb": 32,
        "image": "ubuntu-22.04"
    }

Validate that:
    - cpu_count is bigger than 0 and less than 65
    - mem_size_gb is bigger than 8 and smaller than 1025
    - image is one of "ubuntu-24.04", "debian:bookworm" or "alpine:3.20"

Return a JSON message with new VM id:
    {
        "id": "c9abe3b66fc544c78e355968119081ed"
    }

Stop:

    POST http://localhost:8000/vm/{id}/stop

Validate that {id} is a valid VM id and return a JSON message:
    {
        "id": "c9abe3b66fc544c78e355968119081ed",
        "spec": {
            "cpu_count": 2,
            "mem_size_gb": 32,
            "image": "ubuntu-22.04"
        }
    }
"""
from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import uuid


class VMStartRequest(BaseModel):
    cpu_count: Annotated[int, Field(gt=0, lt=65)]
    mem_size_gb: Annotated[int, Field(gt=8, lt=1025)]
    image: Literal["ubuntu-24.04", "debian:bookworm", "alpine:3.20"]


app = FastAPI()



VM_STORE = dict()


@app.post("/vm/start")
async def start_vm(request: VMStartRequest):
    vm_id = uuid.uuid4().hex
    VM_STORE[vm_id] = {
        "cpu_count": request.cpu_count,
        "mem_size_gb": request.mem_size_gb,
        "image": request.image
    }
    return {"id": vm_id}


@app.post("/vm/{id}/stop")
def stop_vm(id: str):
    if id in VM_STORE:
        return {
            "id": id,
            "spec": VM_STORE[id]
        }
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                        detail="ID not found!")
