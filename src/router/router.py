from fastapi import APIRouter, Depends, Response

import src.router.dependencies as dep

router = APIRouter()


@router.get(
    "/graph",
    name="Получить график",
    response_class=Response,
    responses={
        200: {
            "content": "image/svg"
        }
    }
)
def get_graph(graph_bytes: bytes = Depends(dep.get_graph)):
    return Response(graph_bytes, media_type="image/svg")


@router.get(
    "/spectrum",
    name="Получить спектр",
    response_class=Response,
    responses={
        200: {
            "content": "image/svg"
        }
    }
)
def get_spectrum(graph_bytes: bytes = Depends(dep.get_spectrum)):
    return Response(graph_bytes, media_type="image/svg")

