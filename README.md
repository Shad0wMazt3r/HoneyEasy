# HoneyEasy

## Introduction
HoneyEasy is a honeypot framework that intends to create a honeypot for most major services on a Linux machine. 
HoneyEasy also logs this data and visualizes it in a dashboard for easy analysis.

HoneyEasy is meant for security researchers to observe malicious traffic across the web.

---
## Set Up

HoneyEasy has an easy set up script. However, a few cautionary steps must be taken before setting up HoneyEasy.

1. **Do not run HoneyEasy outside of a virtual machine:** HoneyEasy is meant to be a honeypot, and thus will attract attackers. It takes steps to emulate everything and not allow attackers to access your system. 

    However, NO PROGRAM IS COMPLETELY SAFE AND BUGS MAY EXIST.

2. **Isolate HoneyEasy on the network to prevent lateral movement.**
3. **Always create a new blank virtual machine for an instance of HoneyEasy**

HoneyEasy is intended to be run on debian-based distros. This includes, but is not limited to: Debian, Ubuntu, Linux Mint, Kali Linux, Parrot OS, Raspberry Pi OS etc.

A virtual machine with HoneyEasy already set up is provided here for your convenience: [Click Here](https://github.com/Shad0wMazt3r/HoneyEasy/releases/tag/v0.1.0)

Credentials
```
root:honey
```

A second user is set up for testing

```
honeyeasy:honey
```

It is recommended to set up your own HoneyEasy virtual machine using a debian virtual machine and configuring it yourself.


### Installation Steps

1. Clone the repository:
    `git clone https://github.com/Shad0wMazt3r/HoneyEasy.git`
2. Run the setup script:
    `sudo bash setup.sh`
3. Enjoy

Note: You can use `bash run.sh` after running the setup once. `setup.sh` does that anyway, though. 