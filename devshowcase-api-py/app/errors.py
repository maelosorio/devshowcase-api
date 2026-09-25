"""
Tratamento global de erros.

Em vez de colocar try/except em cada rota, registramos "handlers" globais
uma unica vez (isso e feito no main.py, chamando register_error_handlers).
Toda vez que um desses erros acontecer em QUALQUER rota, o FastAPI intercepta
automaticamente e devolve um JSON padronizado - nunca um stack trace cru.
"""
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ResourceNotFoundError(Exception):
    """Lance isso quando um recurso (perfil, projeto...) pedido pelo ID não existe."""
    def __init__(self, message: str):
        self.message = message


class DuplicateResourceError(Exception):
    """Lance isso quando algo que deveria ser único já existe (ex: e-mail repetido)."""
    def __init__(self, message: str):
        self.message = message


def _corpo_de_erro(status_code: int, error: str, message: str, path: str, erros: list | None = None) -> dict:
    corpo = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": status_code,
        "error": error,
        "message": message,
        "path": path,
    }
    if erros is not None:
        corpo["erros"] = erros
    return corpo


def register_error_handlers(app: FastAPI) -> None:

    # 404 - recurso não encontrado
    @app.exception_handler(ResourceNotFoundError)
    async def handle_not_found(request: Request, exc: ResourceNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=_corpo_de_erro(404, "Recurso Não Encontrado", exc.message, str(request.url.path)),
        )

    # 409 - conflito (ex: e-mail duplicado)
    @app.exception_handler(DuplicateResourceError)
    async def handle_duplicate(request: Request, exc: DuplicateResourceError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=_corpo_de_erro(409, "Recurso Duplicado", exc.message, str(request.url.path)),
        )

    # 400 - dados inválidos enviados pelo cliente (falha nas validações do Pydantic)
    @app.exception_handler(RequestValidationError)
    async def handle_validacao(request: Request, exc: RequestValidationError):
        mensagens = [f"{'.'.join(str(p) for p in erro['loc'][1:])}: {erro['msg']}" for erro in exc.errors()]
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=_corpo_de_erro(
                400, "Dados Inválidos",
                "Um ou mais campos estão inválidos. Veja o campo 'erros'.",
                str(request.url.path), mensagens,
            ),
        )

    # 500 - qualquer outro erro inesperado (nunca expõe o erro real pro cliente)
    @app.exception_handler(Exception)
    async def handle_generico(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_corpo_de_erro(
                500, "Erro Interno do Servidor",
                "Ocorreu um erro inesperado. Tente novamente mais tarde.",
                str(request.url.path),
            ),
        )
