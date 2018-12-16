#!/usr/bin/env python3
"""Compile the apache .conf file."""
import argparse
import sys
import yaml

DEFAULT_CONFIG_FILE = 'config.yaml'

APACHE_CONF_TEMPLATE = '''<VirtualHost *:80>
  ProxyPreserveHost On
  ProxyRequests Off
  ServerName localhost
{aliases}
  ServerAdmin {server_admin}
  ProxyPass /{route} http://localhost:{port}
  ProxyPassReverse /{route} http://localhost:{port}
  ErrorLog ${{APACHE_LOG_DIR}}/error.log
  LogLevel warn
  CustomLog ${{APACHE_LOG_DIR}}/access.log combined
</VirtualHost>
'''

OPTS = None

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('config_file', help='Location of .yaml config file')
  parser.add_argument('out_file', help='Where to write apache .conf file')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  return parser.parse_args()

def make_apache_config(route, port, config):
  aliases = '\n'.join(['  ServerName %s' % alias 
                       for alias in config['server_aliases']])
  return APACHE_CONF_TEMPLATE.format(**{
      'aliases': aliases, 'server_admin': config['server_admin'], 
      'route': route, 'port': port}) 

def main():
  with open(OPTS.config_file) as f:
    config = yaml.load(f)
  with open(OPTS.out_file, 'w') as f:
    for route, port in config['routes']:
      print(make_apache_config(route, port, config), file=f)

if __name__ == '__main__':
  OPTS = parse_args()
  main()

