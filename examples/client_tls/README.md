# TLS in gRPC
gRPC natively support two mode in TLS. We will name them simple TLS and mutual auth TLS in this document.

- [Simple TLS](#simple-tls): daemon starts with its own self-signed certificate and the associated private key. Clients will use this certificate to encrypt communications with daemon.
- [Mutual Authentication TLS](#mutual-authentication-tls): we create our own Certification Authority (CA) to create certificates. We will then create a certificate and a private key for daemon and one per client. Like this client can encrypt communications with daemon, and daemon can verify that client have been authorized to connect.  

# Simple TLS
### Generate certificate and key
Generate server certificate and private key using openssl.

⚠ Replace localhost with daemon hostname. Hostname is the IP address or the domain name clients will use to connect to daemon.

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -days 36500 -out server.pem -nodes -subj '/CN=localhost'
```

### Set up daemon
Pass certificate and private key to daemon using environment variable:
- DAEMON_CERTIFICATE_FILE
- DAEMON_KEY_FILE

If you use docker, create a credentials directory, containing previously generated certificate and key. 
Add this directory as a read-only volume and use environment variable to enable simple TLS in daemon. 

```yaml
  daemon:
    image: olvid/bot-daemon:latest
    environment:
      - OLVID_ADMIN_CLIENT_KEY_CLI=ToSet
      - DAEMON_CERTIFICATE_FILE=./credentials/server.pem
      - DAEMON_KEY_FILE=./credentials/server.key
    ports:
      - 50051:50051
    restart: unless-stopped
    volumes:
      - ./data:/daemon/data
      - ./backups:/daemon/backups
      - ./credentials:/daemon/credentials:ro
```
### Set up client
Your bots will need daemon certificate to encrypt communications.

Assuming your client uses [olvid-bot](https://github.com/olvid-io/Olvid-Bot-Python-Client) python module, you can use three methods to pass certificate file.
We will also consider you created a credentials directory containing previously created files `server.pem`.
If you are in docker ming to mount this directory as a read-only volume.

#### Use environment
Set up three environment variables.
```bash
export OLVID_SERVER_CERTIFICATE_PATH=./credientials/server.pem
```

#### Use files
On start OlvidClient can look for some specific files names to load a tls configuration. To have a persistent TLS configuration (compared to environment), you can create symlinks or copy files to specific locations.
```bash
ln -s ./credentials/server.pem .server.pem
```

#### Use code
Create a GrpcTlsConfiguration object and pass it as an OlvidClient / OlvidBot constructor parameter.
```python
import asyncio
from olvid import OlvidClient

async def main():
    # Implicit configuration, automatically load environment or files configuration if possible.
    client = OlvidClient()
    print(await client.identity_get())

    # TLS simple explicit configuration
    client = OlvidClient(tls_configuration=OlvidClient.GrpcMutualAuthTlsConfiguration(root_certificate_path="./credentials/ca.pem", certificate_chain_path="./credentials/client.pem", private_key_path="./credentials/client.key"))
    print(await client.identity_get())

asyncio.run(main())
```

# Mutual Authentication TLS
### Generate certificates and keys
Generate our local CA (Certification Authority) using openssl.

```bash
openssl req -x509 -new -newkey rsa:2048 -nodes -keyout ca.key -out ca.pem \
  -config ca-openssl.cnf -days 36500 -extensions v3_req
```

Generate server certificate and key.

⚠ Replace localhost with daemon hostname. Hostname is the IP address or the domain name clients will use to connect to daemon.
```bash
# generate server key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out server.key

# generate server certificate
openssl req -new -key server.key -out server.csr -config server-openssl.cnf -subj '/CN=localhost'
openssl x509 -req -CA ca.pem -CAkey ca.key -CAcreateserial -in server.csr \
  -out server.pem -extensions v3_req -extfile server-openssl.cnf -days 36500
```

Generate client certificate and key
```bash
# generate client certificate (you can leave default value)
openssl req -new -key client.key -out client.csr
# set common name to whatever you want that will identify client
openssl x509 -req -CA ca.pem -CAkey ca.key -CAcreateserial -in client.csr \
  -out client.pem -days 36500
```

### Set up daemon

Daemon will need its certificate and key, and the CA to check client are able to connect. We will use three environment variables to specify file paths:
- DAEMON_CERTIFICATE_FILE
- DAEMON_KEY_FILE
- DAEMON_ROOT_CERTIFICATE_FILE

If you use docker, create a credentials directory, containing CA certificate `ca.pem` and server certificate and key `server.pem` and `server.key`.
Add this directory as a read-only volume and use environment variable to enable mutual authentication TLS in daemon.
 
```yaml
  daemon:
    image: olvid/bot-daemon:latest
    environment:
      - OLVID_ADMIN_CLIENT_KEY_CLI=ToSet
      - DAEMON_CERTIFICATE_FILE=./credentials/server.pem
      - DAEMON_KEY_FILE=./credentials/server.key
      - DAEMON_ROOT_CERTIFICATE_FILE=./credentials/ca.pem
    ports:
      - 50051:50051
    restart: unless-stopped
    volumes:
      - ./data:/daemon/data
      - ./backups:/daemon/backups
      - ./credentials:/daemon/credentials:ro
```

### Set up client
Your bots will need their certificate/key pair, and the CA certificate.

Assuming your client uses [olvid-bot](https://github.com/olvid-io/Olvid-Bot-Python-Client) python module, you can use three methods to pass these files path.
We will also consider you created a credentials directory containing previously created files `ca.pem`, `client.pem`, `client.key`. If you are in docker ming to mount this directory as a read-only volume.

#### Use environment
Set up three environment variables.
```bash
export OLVID_ROOT_CERTIFICATE_PATH=./credientials/ca.pem
export OLVID_CERTIFICATE_CHAIN_PATH=./credientials/client.pem
export OLVID_PRIVATE_KEY_PATH=./credientials/client.key
```

#### Use files
On start OlvidClient can look for some specific files names to load a tls configuration. To have a persistent TLS configuration (compared to environment), you can create symlinks or copy files to specific locations.
```bash
ln -s ./credentials/ca.pem .ca.pem
ln -s ./credentials/client.pem .client.pem
ln -s ./credentials/client.key .client.key
```

#### Use code
Create a GrpcTlsConfiguration object and pass it as an OlvidClient / OlvidBot constructor parameter.
```python
import asyncio
from olvid import OlvidClient

async def main():
    # Implicit configuration, automatically load environment or files configuration if possible.
    client = OlvidClient()
    print(await client.identity_get())

    # TLS mutual authentication explicit configuration
    client = OlvidClient(tls_configuration=OlvidClient.GrpcMutualAuthTlsConfiguration(root_certificate_path="./credentials/ca.pem", certificate_chain_path="./credentials/client.pem", private_key_path="./credentials/client.key"))
    print(await client.identity_get())

asyncio.run(main())
```
