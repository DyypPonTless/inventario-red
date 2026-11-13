"""Inventario de red — Práctica 4.

Programación de Redes (E-PRDS-2) · UPQ
Alumno:    Roxana Denice Rodriguez Nieves
Matrícula: 125052994
"""
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI(title="Inventario de red")


class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True


class DispositivoParcial(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None


inventario = [
    Dispositivo(nombre="R1", tipo="router", ip="10.0.0.1"),
    Dispositivo(nombre="SW1", tipo="switch", ip="10.0.0.10", activo=False),
    Dispositivo(nombre="FW1", tipo="firewall", ip="10.0.0.254"),
]


def buscar(nombre: str) -> Dispositivo | None:
    """Devuelve el equipo con ese nombre, o None si no existe."""
    for equipo in inventario:
        if equipo.nombre.upper() == nombre.upper():
            return equipo
    return None


@app.get("/dispositivos")
async def listar():
    """Devuelve todo el inventario."""
    return inventario


@app.get("/dispositivos/{nombre}")
async def obtener(nombre: str):
    """Busca un equipo por su nombre."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(status_code=404,
                            detail=f"No existe el equipo {nombre}")
    return equipo

@app.delete("/dispositivos/{nombre}", status_code=204)
async def eliminar(nombre: str):
    """Da de baja un equipo del inventario."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(status_code=404,
                            detail=f"No existe el equipo {nombre}")
    inventario.remove(equipo)
    return Response(status_code=204)