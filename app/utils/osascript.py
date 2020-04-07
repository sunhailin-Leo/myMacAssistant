import os
from typing import Union, Optional, Sequence

from app.blueprints import logger


class ExecuteWayEnum:
    SystemNotification: str = "notify"
    IPAddress: str = "ip"

    ExecuteWayIndex: Sequence[str] = ["notify", "ip"]


class OsaScriptExecutor:
    def __init__(self, way: Union[ExecuteWayEnum, str] = ""):
        self._way = way
        if self._way == "" or self._way not in ExecuteWayEnum.ExecuteWayIndex:
            raise ValueError("OsaScriptExecutor argument way is error!")

    @staticmethod
    def _core_run_command(command: str) -> Sequence[str]:
        r = os.popen(command)
        info = r.readlines()
        r.close()
        return info

    def run_notification_script(
        self,
        title: str,
        content: str,
        subtitle: Optional[str] = None,
    ):
        if subtitle is None:
            sub_command = f"\"{content}\" with title \"{title}\""
        else:
            sub_command = f"\"{content}\" with title \"{title}\" subtitle \"{subtitle}\""
        main_command = f"osascript -e 'display notification {sub_command}'"
        logger.info("执行的 osascript: {command}", command=main_command)
        self._core_run_command(command=main_command)

    def run_ip_address_info_script(self):
        command = "osascript -e 'IPv4 address of (system info)'"
        result = self._core_run_command(command=command)
        result = "".join([d.replace("\n", "") for d in result])
        if "local" in result:
            return "127.0.0.1"
        return result
