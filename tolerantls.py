#!/usr/bin/env python2

import socket
import scapy
from scapy_ssl_tls.ssl_tls import *
import argparse

def main():
  # Parse arguments
  parser = argparse.ArgumentParser(description='Test a TLS server for version intolerance.')

  parser.add_argument('--host', help='Host to conect to', required=True)
  parser.add_argument('--port', help='Port to connect to (default: 443)', default=443, type=int)

  args = parser.parse_args()

  target = (args.host, args.port)

  print('[*] Testing TLS version intolerance against {0}:{1}'.format(args.host, args.port))

  # create tcp socket
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.connect(target)

  p = TLSRecord()/TLSHandshake()/TLSClientHello(version=0x03EE, cipher_suites=range(0xff), compression_methods=range(0xff)[::-1])

  s.sendall(str(p))
  resp = s.recv(8192)
  s.close()

  resp = SSL(resp)

  if resp.haslayer(TLSServerHello):
    v = resp[TLSServerHello].version

    print("[+] Server is not intolerant - it downgraded the client request and proposed to use %s" % (TLS_VERSIONS.get(v, v)))
  else:
    print("[-] Server is TLS version intolerant")

if __name__ == "__main__":
    main()
