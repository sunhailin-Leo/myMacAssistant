<h1 align="center">myMacAssistant</h1>
<p align="center">
    <em>Try to be the best assistant to control your MacBook Pro by using your smartphone.</em>
</p>
<p align="center">
    <a href="https://travis-ci.org/sunhailin-Leo/myMacAssistant">
        <img src="https://api.travis-ci.org/sunhailin-Leo/myMacAssistant.svg?branch=master" alt="Travis Build Status">
    </a>
    <a href="https://ci.appveyor.com/project/sunhailin-Leo/mymacassistant">
        <img src="https://ci.appveyor.com/api/projects/status/djxidi0n7klwcggh/branch/master?svg=true" alt="Appveyor Build Status">
    </a>
    <a href="https://codecov.io/gh/sunhailin-Leo/myMacAssistant">
      <img src="https://codecov.io/gh/sunhailin-Leo/myMacAssistant/branch/master/graph/badge.svg?token=94AT4GFF33" />
    </a>
</p>
<p align="center">
    <a href="https://github.com/sunhailin-Leo/myMacAssitant/pulls">
        <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" alt="Contributions welcome">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License">
    </a>
</p>

## 📣 Info

* Try to use everything to achieve the best assistant!

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

# Run the server (Only MacOS)
$ python3 server.py
```

## ⏳ ChangeLog

* 2020-04-07 v1.0.0:
    * Finish some important api
    * Develop by Flask


## ⛏ Code Quality

### Unit test

```shell
$ sh test.sh
```

### Integration test

Use [Travis CI](https://travis-ci.org/) and [AppVeyor](https://ci.appveyor.com/) CI environment.

## 📃 License

MIT [©sunhailin-Leo](https://github.com/sunhailin-Leo)
