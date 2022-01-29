# Introduction
Smilin' File Hosting is a Zero Knowledge file hosting service written in Python. I wrote this as a hobby project for
my cousins, and it's turned into something a lot more cool.

## Installation
This program has two parts, the Server (main API) and the Client.

### Server
To run the server, install Docker (specifically, docker-compose).

=== "Windows"

    You have to install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

=== "Linux"
    
    First, install Docker and then run this;<br>
    `sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

=== "MacOS"

    Install homebrew, if it's not installed and then run this;<br>
    `brew install docker-compose` 

Afterwards, open up a Terminal and `cd` to the 'server/' directory and run<br>
`docker-compose up -d`

This creates two containers;

- A Python Container (The Main API)
- A MySQL Container (The Main Database)

The Python Container contains the main server, which exposes Port 2356, and the
MySQL Container contains a MySQL Database with the user and password specified in the docker-compose file.

### Client
To run the client, you'll need a python interpreter. The program was written using Python 3.10, so install either 3.10
or any version above 3.10. You may download it from [here](https://www.python.org/downloads/).

Afterwards, `cd` to the 'client/', create a virtual environment[^1] and install the requirements. To do this, run;

[^1]:   Instead of using the system-wide or local interpreter, it's safer and more efficient to use a virtual
        environment.<br>Note that you don't have to use python's "venv", you can even use an Anaconda Environment.


=== "Windows"
    `python -m venv ./venv/`

    `./venv/Scripts/activate`

    `python -m pip install -r requirements.txt`

=== "Linux and MacOS"
    `python3 -m venv ./venv/`

    `source ./venv/bin/activate`

    `python3 -m pip install -r requirements.txt`

This installs all the packages required by the Client to the virtual environment.

After installing the requirements, you need to install GPG (GNU Privacy Guard), which is essential for the 
encryption part. You may download it from [here](https://gnupg.org/download/index.html). After installing, GPG, you
need to generate a Key Pair. As this is a process that's not that straightforward, here's a [guide](https://www.redhat.com/sysadmin/creating-gpg-keypairs)
to follow. But here are my preferences and options essential for the program to function properly;

* `Kind of key` -> RSA and RSA (NEEDED)
* `Size` -> Any size, I'd recommend a high amount (>=2048)
* `Email` -> This is the same email that you'll use when running the program, so choose wisely

You may finally run the program by typing;

=== "Windows"

    `python main.py`

=== "Linux and MacOS"

    `python3 main.py`