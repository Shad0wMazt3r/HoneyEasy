# HoneyEasy

HoneyEasy is a lightweight, configurable SSH and HTTP honeypot for isolated Linux labs. It records login attempts and web requests while serving believable decoy content for security research, education, and traffic analysis.

> [!WARNING]
> HoneyEasy is an experimental research tool, not a security boundary. Run it only on a disposable virtual machine that is isolated from trusted networks. It records credentials, request headers, and POST bodies in plaintext, so protect and routinely remove its logs.

## What it captures

| Service | Current behavior | Default logs |
| --- | --- | --- |
| SSH | Records attempted usernames and passwords, accepts configured decoy credentials, and presents a small fake shell | `logs/log_ssh`; unrecognized commands in `ssh_honeypot.log` |
| HTTP | Serves files from `www/` and records GET paths, request headers, POST headers, and POST bodies | `logs/log_http` |

The fake SSH shell responds to a limited set of commands, including `whoami`, `id`, `uname -a`, `pwd`, `ls`, `cd`, and `cat`. The bundled web lure presents an under-construction site with a discoverable debug page.

## Project status

HoneyEasy is an early prototype. SSH and plain HTTP listeners are implemented. HTTPS, a log-analysis dashboard, log rotation, retention controls, and production-grade process supervision are not yet included.

## Safety first

- Use a new, disposable virtual machine.
- Place the VM on a dedicated, restricted network with no route to sensitive systems.
- Do not reuse real usernames, passwords, files, host keys, or web content as lures.
- Review firewall and port-forwarding rules before exposing either listener.
- Treat all captured data as sensitive.
- Change the passwords on the prebuilt release image before connecting it to any network. Its published defaults are intentionally public and provide no protection.
- Operate HoneyEasy only on systems and networks you own or are authorized to monitor.

## Requirements

- A Debian-based Linux distribution such as Debian, Ubuntu, Linux Mint, Kali Linux, Parrot OS, or Raspberry Pi OS
- Python 3
- Root privileges when binding the default SSH port (`22`)

## Install and run

Clone the repository and run the setup script inside the isolated VM:

```bash
git clone https://github.com/Shad0wMazt3r/HoneyEasy.git
cd HoneyEasy
sudo bash setup.sh
```

The setup script installs the required system packages, installs Paramiko, and starts both listeners. After the first setup, start them again with:

```bash
sudo bash run.sh
```

The script prints both process IDs. Stop the listeners with your normal process supervisor or by terminating those process IDs.

### Prebuilt lab image

A preconfigured virtual machine is available in the [v0.1.0 release](https://github.com/Shad0wMazt3r/HoneyEasy/releases/tag/v0.1.0). It is provided for disposable lab use only. Change its default passwords before networking the VM:

```text
root:honey
honeyeasy:honey
```

Building a fresh VM from this repository is recommended.

## Configure the lures

Runtime settings live in `.config_honeyeasy`.

| Setting | Description | Default |
| --- | --- | --- |
| `SSH_PORT` | Port used by the SSH honeypot | `22` |
| `HTTP_PORT` | Port used by the HTTP honeypot | `8080` |
| `SSH_DIRECTORY` | Directory exposed by fake `ls` and `cat` commands | `user` |
| `HTTP_DIRECTORY` | Directory served by the HTTP listener | `www` |
| `SSH_KEY` | Path to the generated SSH host key | `ssh_honeypot.key` |
| `SSH_BANNER` | Banner shown after a successful decoy login | bundled warning banner |
| `SSH_LOG` | SSH log filename inside `logs/` | `log_ssh` |
| `HTTP_LOG` | HTTP log filename inside `logs/` | `log_http` |
| `SSH_CREDS` | Colon-delimited credentials accepted by the fake SSH service | `user/creds.txt` |

`HTTPS_PORT` and `HTTPS_LOG` are reserved configuration values; the current version does not start an HTTPS listener.

### Customize the SSH lure

- Add decoy files to `user/`. They become visible through the fake `ls` and `cat` commands.
- Edit `user/creds.txt` to select which decoy username/password pairs are accepted.
- Change `SSH_BANNER` to match the system persona you want to emulate.

The `user/README` file describes a fictional project on purpose. It is lure content, not HoneyEasy documentation.

### Customize the web lure

Replace or extend the content in `www/`. The bundled `robots.txt` advertises paths that may attract automated probes, while `www/debug/` supplies a simple decoy form.

## Review captured activity

Logs are appended as plain text:

```bash
tail -f logs/log_ssh
tail -f logs/log_http
tail -f ssh_honeypot.log
```

SSH logs include attempted credentials; unrecognized fake-shell commands are written separately to `ssh_honeypot.log`. HTTP logs may include cookies, authorization headers, form fields, and arbitrary POST content. Store them only as long as your research requires.

## Repository layout

| Path | Purpose |
| --- | --- |
| `ssh_honeypot.py` | Paramiko-based SSH listener and fake shell |
| `web_honeypot.py` | Static HTTP listener and request logger |
| `.config_honeyeasy` | Listener, lure, credential, banner, and log settings |
| `run.sh` | Starts the SSH and HTTP processes |
| `setup.sh` | Installs Debian dependencies and performs the first run |
| `user/` | Files and credentials used by the SSH lure |
| `www/` | Static content used by the HTTP lure |
| `logs/` | Local captured activity |

## Known limitations

- The SSH shell emulates only a small command set; it is not a full system sandbox.
- HTTPS/TLS is not implemented.
- There is no dashboard or built-in log search.
- Logs are plaintext and have no automatic rotation or retention policy.
- The launch script does not restart failed listeners or manage them as services.
- This prototype has not been hardened for unattended internet exposure.
