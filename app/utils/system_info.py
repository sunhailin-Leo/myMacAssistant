import time
from typing import Dict, Optional, Sequence

import psutil

from app.utils import synchronized


class UnitTransferEnum:
    BytesToKB: int = 2 << 10 - 1
    BytesToMB: int = 2 << 20 - 1
    BytesToGB: int = 2 << 30 - 1
    BytesToTB: int = 2 << 40 - 1


class MemoryUnitInfoMode:
    Normal: str = "NORMAL"
    Kilobyte: str = "KB"
    MegaByte: str = "MB"
    Gigabyte: str = "GB"
    Terabyte: str = "TB"
    InfoIndex: Sequence[str] = ["NORMAL", "KB", "MB", "GB", "TB"]


class SystemInfo:
    _instance = None

    def __init__(self):
        self._mapper: dict = self._lazy_mapper_from_unit_to_mode()

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _lazy_mapper_from_unit_to_mode() -> dict:
        return {
            MemoryUnitInfoMode.Normal: 1,
            MemoryUnitInfoMode.Kilobyte: UnitTransferEnum.BytesToKB,
            MemoryUnitInfoMode.MegaByte: UnitTransferEnum.BytesToMB,
            MemoryUnitInfoMode.Gigabyte: UnitTransferEnum.BytesToGB,
            MemoryUnitInfoMode.Terabyte: UnitTransferEnum.BytesToTB,
        }

    @staticmethod
    def _format_unit(data: int, unit: int) -> float:
        return round(data / unit, 2)

    def get_memory_info(self, mode: str = MemoryUnitInfoMode.Normal) -> Optional[Dict]:
        mem_info = psutil.virtual_memory()
        mode = mode.upper()
        if mode not in MemoryUnitInfoMode.InfoIndex:
            return None

        # 总内存
        total = mem_info.total
        # 可用内存
        available = mem_info.available
        # 使用率
        percent = mem_info.percent
        # # 已使用内存
        # used = mem_info.used
        # # 可用内存
        # free = mem_info.free
        # # 正在使用或刚被使用
        # active = mem_info.active
        # # 内存占用有效，但可能最近没被使用
        # inactive = mem_info.inactive
        # # 核心占用
        # wired = mem_info.wired
        return {
            "total": self._format_unit(total, self._mapper[mode]),
            "available": self._format_unit(available, self._mapper[mode]),
            "percent": percent,
        }

    @staticmethod
    def get_user_info():
        format_user_info = []
        user_info_list = psutil.users()
        for user in user_info_list:
            user_format = {
                "name": user.name,
                "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.started))
            }
            format_user_info.append(user_format)
        return format_user_info


if __name__ == '__main__':
    s = SystemInfo()
    print(s.get_memory_info(mode="GB"))
    # s.get_user_info()
