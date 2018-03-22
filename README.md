tolerantls: A scapy-based tester for TLS version intolerance
============================================================

TLS specifies that when a client offers a TLS version that is higher than
the version the server supports, the server should propose to use the
maximum version it knows how to handle.

Servers which incorrectly handle TLS version negotiation just close the
connection if they receive an unknown TLS version, something known as being
[TLS version intolerant](https://security.stackexchange.com/questions/66782/what-is-tls-version-intolerance).

These servers force browsers to implement falbacks that force them to try to
connect multiple times, affecting throughput and browser experience and,
more importantly, enable a mitm-attacker to selectively reset the
negotiation of strong protocols, forcing the user of weaker protocols that
simplify breaking the security of the connection.

This tool allows you to check if a specific TLS server is version
intolerant. It is loosely based on examples provided by the [scapy ssl/tls module](https://github.com/tintinweb/scapy-ssl_tls)

Requirements
------------

**IMPORTANT: There are quite [a few incompatibilities][scapy-ssl-tls-version-issue] between different versions of scapy and scapy-ssl_tls, we strongly recommend you
stick to the specific package versions**

scapy and its tls library do the heavy lifting here, so you need to have these installed:

```
  $ pip install 'scapy>=2.2.0,<2.3.3' 'scapy-ssl_tls==1.2.3'
```

scapy and scapy-ssl-tls are currently only available for python2, so you cannot use python3 with tolerantls.

Usage
-----

The application accepts two parameters, the mandatory `host` to test and an optional `port` which default to 443/tcp if not specified:

```
  $ tolerantls.py -h
  usage: tolerantls.py [-h] --host HOST [--port PORT]

  Test a TLS server for version intolerance.

  optional arguments:
    -h, --help   show this help message and exit
    --host HOST  Host to conect to
    --port PORT  Port to connect to (default: 443)
```

For instance to test the TLS version tolerance of example.com:

```
  $ tolerantls.py --host example.com
  [*] Testing TLS version intolerance against example.com:443
  [+] Server is not intolerant - it downgraded the client request and proposed to use TLS_1_2
```

[scapy-ssl-tls-version-issue]: https://github.com/tintinweb/scapy-ssl_tls/issues/69#issuecomment-250086682
