from fastapi import APIRouter, Depends

import src.router.dependencies as dep

router = APIRouter()


@router.get(
    "/graph",
    name="Получить график",
    response_model=bytes,
)
def get_graph(graph_bytes: bytes = Depends(dep.get_graph)):
    return graph_bytes

