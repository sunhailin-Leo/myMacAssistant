import sys
import logging
import platform
from pathlib import Path

from flask import Flask
from loguru import logger

from app.blueprints import (
    call_401,
    call_403,
    call_404,
    call_405,
    call_500,
    InterceptHandler,
)
from app.blueprints.device_blueprint import device


app = Flask(__name__)


@app.errorhandler(401)
def error_401(error):
    return call_401(error)


@app.errorhandler(403)
def error_403(error):
    return call_403(error)


@app.errorhandler(404)
def error_404(error):
    return call_404(error)


@app.errorhandler(405)
def error_405(error):
    return call_405(error)


@app.errorhandler(500)
def error_500(error):
    return call_500(error)


class InitServer:
    def __init__(
        self,
        host: str,
        port: int,
        debug_mode: bool = True,
        log_name: str = "assistant_server.log",
    ):
        self._host = host
        self._port = port
        self._debug_mode = debug_mode
        self._log_name = log_name

        self._app = app
        self._init_blueprint()
        self._init_logger()

    def _init_blueprint(self):
        self._app.register_blueprint(device, url_prefix="/device")

    def _init_logger(self):
        path = Path("./logs")
        if not path.exists():
            path.mkdir(parents=True)
        log_name = Path(path, self._log_name)
        logging.basicConfig(
            **{"handlers": [InterceptHandler(level="INFO")], "level": "INFO"}
        )
        logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])  # 配置日志到标准输出流
        logger.add(
            log_name,
            rotation="500 MB",
            encoding="utf-8",
            colorize=False,
            level="INFO",
            retention="7 days",
            compression="zip",
            format="<green>{time}</green> <level>{message}</level>",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

    def run(self):
        self._app.run(host=self._host, port=self._port, debug=self._debug_mode)


def is_macos() -> bool:
    return "Darwin" in platform.platform()


if __name__ == "__main__":
    if is_macos():
        InitServer(host="127.0.0.1", port=10086, debug_mode=False).run()
    else:
        exit(1)
