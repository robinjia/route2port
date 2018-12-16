#!/usr/bin/env python3
"""Compile the apache .conf file."""
import argparse
import sys
import yaml

APACHE_HEADER_TEMPLATE = '''<VirtualHost *:80>
  ProxyPreserveHost On
  ProxyRequests Off
  ServerName localhost
{aliases}
  ServerAdmin {server_admin}
  ErrorLog ${{APACHE_LOG_DIR}}/error.log
  LogLevel warn
  CustomLog ${{APACHE_LOG_DIR}}/access.log combined
  RewriteEngine On
  ProxyHTMLEnable On
  ProxyHTMLInterp On
'''
APACHE_ROUTE_TEMPLATE='''  ProxyPass /{route} http://localhost:{port}
  ProxyPassReverse /{route} http://localhost:{port}
  ProxyHTMLURLMap ^/ /{route}/ [R] "%{{REQUEST_URI}} =~ m#^/{route}(/.*)?$#"
  RewriteRule ^/{route}$ /{route}/ [R]
'''
APACHE_FOOTER='</VirtualHost>'

OPTS = None

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('config_file', help='Location of .yaml config file')
  parser.add_argument('out_file', help='Where to write apache .conf')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  return parser.parse_args()

def make_header(config):
  aliases = '\n'.join(['  ServerName %s' % alias 
                       for alias in config['server_aliases']])
  return APACHE_HEADER_TEMPLATE.format(**{
      'aliases': aliases, 'server_admin': config['server_admin']})

def make_route_config(route, port):
  return APACHE_ROUTE_TEMPLATE.format(**{'route': route, 'port': port})

def main():
  with open(OPTS.config_file) as f:
    config = yaml.load(f)
  with open(OPTS.out_file, 'w') as f:
    print(make_header(config), file=f)
    for route, port in config['routes']:
      print(make_route_config(route, port), file=f)
    print(APACHE_FOOTER, file=f)

if __name__ == '__main__':
  OPTS = parse_args()
  main()

