import os
from typing import Dict, List


class _BluetoothInfo:
    def __init__(self):
        self._cmd: str = "system_profiler SPBluetoothDataType"
        self._data: List[Dict] = []
        self._level_map: List = []

    def __call__(self, *args, **kwargs) -> List:
        return self._bluetooth_rssi_get()

    def _bluetooth_rssi_get(self) -> List:
        devices = self._get_bluetooth_devices(self._cmd)

        for device_name, device_info in devices.items():
            self._data.append({"name": device_name, "info": device_info})
        return self._data

    def _get_bluetooth_devices(self, cmd: str):
        # 执行命令获取所有蓝牙相关信息
        r = os.popen(cmd)
        info = r.readlines()  # 读取命令行的输出到一个list
        self._process_info(info=info)
        r.close()
        return self._level_map2dict(t_tree=self._level_map)["Bluetooth"][
            "Devices (Paired, Configured, etc.)"
        ]

    def _process_info(self, info: List):
        # 处理命令行结果，生成根据缩进判定的层级
        for line in info:  # 按行遍历
            line = line.strip("\r\n")
            if len(line) > 0:  # 第二行是空行
                line_info = self._get_line_info(line=line)
                if line_info["level"] >= 0:
                    # 把第一行 Bluetooth 去除
                    self._level_map.append(line_info)

    @staticmethod
    def _get_line_info(line: str):
        # 解析命令行每行信息
        split = line.split(":")
        name = split[0].lstrip(" ")
        value = split[1].lstrip(" ")
        level = (len(line) - len(line.lstrip(" ")) - 2) / 4
        if level < 0:
            level = 0  # 针对第一行

        line_info: Dict = {"name": name, "value": value, "level": level}
        return line_info

    def _level_map2dict(self, t_tree: List, level: int = 0) -> Dict:
        # 根据层级信息转化成字典结构
        result: Dict = {}
        for i in range(0, len(t_tree)):
            current_node = t_tree[i]
            try:
                next_node = t_tree[i + 1]
            except IndexError:
                next_node = {"level": -1}

            # 边界条件，非当前层级
            if current_node["level"] > level:  # 已经作为整体插入，跳过
                continue
            if current_node["level"] < level:  # 当前是上一级的，直接返回现有结果
                return result

            # 递归生成
            if next_node["level"] == level:  # 同级
                self._dict_insert_or_append(
                    a_dict=result,
                    key=current_node["name"],
                    val=current_node["value"],
                )
            elif next_node["level"] > level:  # 下一级，将下一级整体插入
                next_level = self._level_map2dict(
                    t_tree=t_tree[(i + 1):], level=next_node["level"]
                )
                # 剩下的进行处理
                self._dict_insert_or_append(
                    a_dict=result,
                    key=current_node["name"],
                    val=next_level,
                )
            else:  # 下一个是上一级的，当前插入完成直接返回
                self._dict_insert_or_append(
                    a_dict=result,
                    key=current_node["name"],
                    val=current_node["value"],
                )
                return result
        return result

    @staticmethod
    def _dict_insert_or_append(a_dict: Dict, key: str, val: Dict):
        # 针对key是否存在，新增或者添加
        if key in a_dict:  # 添加
            if isinstance(a_dict[key], List) is not True:
                # 将单独存在的转化成list
                a_dict[key] = [a_dict[key]]
            a_dict[key].append(val)
        else:
            # 新增
            a_dict[key] = val


BluetoothInfo = _BluetoothInfo()
