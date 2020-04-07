import logging
from typing import Dict, List, Union, Optional

from flask import jsonify
from loguru import logger
from merry import Merry


class CustomResponse:
    def __init__(self):
        self._success_code: str = "000000"
        self._failure_code: str = "999999"

    @staticmethod
    def _public_response(
            code: Union[str],
            msg: Optional[str],
            data: Optional[List] = None,
    ) -> dict:
        return {"retCode": code, "retMsg": msg, "retData": data}

    def success_response(
            self,
            code: Union[str] = "000000",
            msg: Optional[str] = "",
            data: Optional[List] = None,
    ) -> dict:
        return self._public_response(code=code, msg=msg, data=data)

    def error_response(
            self,
            code: Union[str] = "999999",
            msg: Optional[str] = "",
            data: Optional[List] = None,
    ) -> dict:
        return self._public_response(code=code, msg=msg, data=data)

    def response_route(self, response: Dict) -> Dict:
        """
        返回对象分类路由
        :param response: 返回对象
        :return: 分类后返回的字典
        """
        if response.get("status", None) == "success":
            return self.success_response(
                msg=response.get("msg", ""), data=response.get("data", None)
            )
        else:
            if response.get("code") is not None:
                return self.error_response(
                    msg=response.get("msg", ""), data=response.get("data", None)
                )
            return self.error_response(
                msg=response.get("msg", ""), data=response.get("data", None)
            )


response_route = CustomResponse().response_route

_merry = Merry(logger_name="exception_logger")
MerryExcept = _merry._except
MerryTry = _merry._try


@MerryExcept(Exception)
def all_exception_handler(err):
    logger.error(err)
    return jsonify(response_route({"msg": "请求异常"}))


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


class _HTTErrorHandler:
    def __init__(self, msg: str):
        self._msg = msg

    def __call__(self, *args, **kwargs):
        error = args[0]
        logger.error(f"[Request Error] Code: {error.code}; Message: {error.description}")
        return jsonify(response_route({"msg": self._msg}))


class _HTTPError401(_HTTErrorHandler):
    pass


class _HTTPError403(_HTTErrorHandler):
    pass


class _HTTPError404(_HTTErrorHandler):
    pass


class _HTTPError405(_HTTErrorHandler):
    pass


class _HTTPError500(_HTTErrorHandler):
    pass


call_401 = _HTTPError401(msg="Unauthorized")
call_403 = _HTTPError403(msg="Forbidden")
call_404 = _HTTPError404(msg="404 Not Found")
call_405 = _HTTPError405(msg="Method Not Allow")
call_500 = _HTTPError500(msg="Server Error")
