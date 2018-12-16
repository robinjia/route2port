# route2port
Easily set up routing from a URL to a port on the local machine, through apache.

## Requirements:
- Ubuntu 18.04 (likely to work on similar operating systems, but has not been tested)
- Python 3

## Setup:
1. Install apache, e.g. for Ubuntu:

    sudo apt-get install apache2

2. Install python3 requirements:

    pip3 install -r requirements.txt

3. Enable necessary apache modules:

    sudo a2enmod ssl proxy proxy_balancer proxy_http

## Basic use
1. Copy the example files from the `example` directory to the root of this repository:

    cp example/* .

2. Edit `config.yaml` to have the correct information for your system, and the appropriate mappings.

3. Initialize 

    ./route2port init

4. If you edit `config.yaml`, run the following to update:

    ./route2port update
