<h1 align="center">myMacAssistant</h1>
<p align="center">
    <em>Try to be the best assistant to control your MacBook Pro by using your smartphone.</em>
</p>

## 📣 Info

* Try to use everything to achieve the best assistant!

## ⏳ Update Version

* 2020-04-07 v1.0.0:
    * Finish some important api
    * Develop by Flask
    
## 📖 Api Example

Interface | Function | Request Method | Parameters  
-|-|-|-
/device/getBluetoothStatus | Get all bluetooth info | POST | None |
/device/getIPAddress | Get current connect IP Address | POST | None |
/device/getUserInfo | Get current computer user info | POST | None
/device/getMemoryInfo | Get current computer memory usage | POST | JSON {"mode": <MemoryUnitInfoMode: ["NORMAL", "KB", "MB", "GB", "TB"]>}
/device/makeNotification | Post message to your computer | POST | JSON {"title": str, "content": "<Limit 50 characters>", "subtitle": "< Optional parameters >"}


## 🔰 Install

```shell script
# Clone the project
$ git clone https://github.com/sunhailin-Leo/myMacAssistant.git

# Switch to the project path
$ cd app

# Run the server (Unix / MacOS)
$ python3 server.py

# Run the server (Windows)
$ python server.py 
```

## ⛏ Code Quality

### Unit test

```shell
$ sh test.sh
```

### Integration test

Use [Travis CI](https://travis-ci.org/) and [AppVeyor](https://ci.appveyor.com/) CI environment.

## 📃 License

MIT [©sunhailin-Leo](https://github.com/sunhailin-Leo)
