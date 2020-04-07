from flask import Blueprint, jsonify, request

from app.blueprints import logger, MerryTry, response_route
from app.utils.bluetooth import BluetoothInfo
from app.utils.chrome import ChromeBookmarksParser
from app.utils.osascript import ExecuteWayEnum, OsaScriptExecutor
from app.utils.system_info import SystemInfo

device = Blueprint("device", __name__)


@device.route("/getBluetoothStatus", methods=["POST"])
@MerryTry
def get_bluetooth_status():
    logger.info(f"当前访问接口: {request.path}")
    result = BluetoothInfo()
    return jsonify(response_route({"status": "success", "data": result, "msg": "请求成功"}))


@device.route("/getIPAddress", methods=["POST"])
@MerryTry
def get_ip_address():
    logger.info(f"当前访问接口: {request.path}")
    result = (
        OsaScriptExecutor(way=ExecuteWayEnum.IPAddress)
        .run_ip_address_info_script()
    )
    return jsonify(response_route({"status": "success", "data": result, "msg": "请求成功"}))


@device.route("/getUserInfo", methods=["POST"])
@MerryTry
def get_memory_info():
    logger.info(f"当前访问接口: {request.path}")
    system = SystemInfo()
    return jsonify(response_route({
        "status": "success",
        "data": system.get_user_info(),
        "msg": "请求成功",
    }))


@device.route("/getMemoryInfo", methods=["POST"])
@MerryTry
def get_user_info():
    logger.info(f"当前访问接口: {request.path} 请求参数: {request.json}")
    mode = request.json.get("mode")
    if mode is None:
        return jsonify(response_route({"msg": "参数异常"}))
    system = SystemInfo()
    return jsonify(response_route({
        "status": "success",
        "data": system.get_memory_info(mode=mode),
        "msg": "请求成功",
    }))


@device.route("/makeNotification", methods=["POST"])
@MerryTry
def make_system_notification():
    logger.info(f"当前访问接口: {request.path} 请求参数: {request.json}")
    title = request.json.get("title")
    content = request.json.get("content")
    subtitle = request.json.get("subtitle")
    if title is not None and content is not None and len(content) <= 50:
        (
            OsaScriptExecutor(way=ExecuteWayEnum.SystemNotification)
            .run_notification_script(title=title, content=content, subtitle=subtitle)
        )
        return jsonify(response_route({
            "status": "success",
            "data": None,
            "msg": "请求成功",
        }))
    return jsonify(response_route({"msg": "参数异常"}))


@device.route("/getChromeBookmarks", methods=["POST"])
@MerryTry
def get_chrome_bookmarks():
    logger.info(f"当前访问接口: {request.path}")
    data = (
        ChromeBookmarksParser()
        .load_bookmarks()
        .get_data()
    )
    return jsonify(response_route({"status": "success", "data": data, "msg": "请求成功"}))
