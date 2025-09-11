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
from enum import Enum
from http import HTTPStatus
from threading import Lock
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

lock = Lock()
VM_STORE = {}  # id -> VM


app = FastAPI()


class Image(Enum):
    ubuntu = 'ubuntu:24.04'
    debian = 'debian:bookworm'
    alpine = 'alpine:3.20'


class VM(BaseModel):
    cpu_count: int = Field(gt=0, lt=65)
    mem_size_gb: int = Field(ge=8, lt=1025)
    image: Image


@app.post('/vm/start')
def start_vm(vm: VM):
    id = uuid4().hex
    with lock:
        VM_STORE[id] = vm
    return {'id': id}


@app.post("/vm/{id}/stop")
def stop_vm(id: str):
    with lock:
        if id in VM_STORE:
            return {
                "id": id,
                "spec": VM_STORE[id]
            }
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                        detail="ID not found!")
