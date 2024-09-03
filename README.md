**Olvid Bots Quickstart**

# Introduction

This repository contains the procedures to set up automated tools in Olvid. They could be used to implement a chatbot, an alerting system, or any program interacting with Olvid using our API.

Olvid is an open-source private and secure messaging application available for all major platforms (Android, iOS, macOS, Windows, Linux):

[Download Olvid Here](https://olvid.io/download/)

Note that the use of this framework is part of Olvid's paying features. You can use this repository to test and deploy the possibilities offered by this framework, but if you want to use it without limitations, please [contact the Olvid team](https://olvid.io/contact/).

# Terminology
Here are a few specific terms we will use in this repository.
* **Daemon**: a standalone and fully manageable Olvid application exposing gRPC services to control it.
* **CLI (Command-Line Interface)**: a text-based interface to setup and manually interact with a daemon instance.
* **Bot/Client**: a program that interacts with a daemon instance, acting as an Olvid user.
* **Identity**: an Olvid profile hosted in a daemon.
* **Client Key**: a unique identifier used to authenticate with the Olvid API. A client key is associated with an identity and only gives a client the permission to manage this identity.
* **API Key**: a key given by the Olvid team to let you use this framework without limitations. This key is set up once.

# Protobuf and gRPC
To maximize the versatility of our daemon, we employed the gRPC framework, which enables it to expose a server API that can be accessed by client code generated in numerous programming languages. We developed a higher-level library in Python, but it is entirely feasible to generate client code in other languages. As this falls outside the scope of this documentation, we will not delve into the subject here. Instead, you can find more information and the protobuf and gRPC source files in our [protobuf repository](https://github.com/olvid-io/Olvid-Bot-Protobuf).

# Python module
To make it easier to get you started, we have developed a high-level Python library implementing all the main features offered by the gRPC API. This allows users to focus on their specific use case, without worrying about the intricacies of gRPC services or the Olvid API.

This Olvid Python module provides two main classes: `OlvidClient` and `OlvidBot`. These classes implement all the methods exposed by a daemon, giving you complete control over its capabilities, but they also include additional mechanisms to simplify your code for the most common use cases.
The sources for this Python module can be found in our [Olvid Bot Python Client repository](https://github.com/olvid-io/Olvid-Bot-Python-Client) and the module itself available as a [PyPi module](https://pypi.org/project/olvid-bot/).

Some examples of generic Olvid automation use cases relying on this Python module can be found in our [examples](./examples) directory.

Furthermore, this module includes a Command-Line Interface (CLI) that enables easy setup and manual control of a daemon.
Its functionality for setting up a daemon is described in our [installation guide](./quickstart/INSTALL.md).
You can find the complete CLI reference [here](https://github.com/olvid-io/Olvid-Bot-Python-Client)

# Installation
This project was designed to run in Docker containers. The procedure to deploy and set up docker environment is described in details in this [INSTALL](./quickstart/INSTALL.md) file.

# Security Considerations
When using these products, please be mindful of the following security considerations:

- **Unencrypted Communications**: note that the exchanges between clients and the daemon are currently not encrypted. Please make sure to secure your network communications between the two to avoid unwanted access by third parties.
- **Cleartext Authentication**: as a consequence of the aforementioned point, the authentication mechanism provided by client keys cannot currently be considered as a valid source of trust. Since the traffic is in plaintext, a malicious client could easily intercept another client's key and impersonate it. Thus, client keys should be viewed as a gatekeeper for controlling only your associated identity, rather than a real security element.
- **Daemon and client own your exchanges**: the daemon relays and potentially stores all messages addressed to it (directly or within groups). This poses a risk to the confidentiality of your exchanges on Olvid if the daemon and its clients are not deployed in a properly secured environment. However, by design, a daemon does not need to be exposed on the internet if its clients connect directly to it. In most cases, it is possible to hide the daemon behind an extremely restrictive firewall.

# Contributing to Olvid
Olvid, as a company, has not yet put in place all the necessary processes to easily accept external contributions. In particular, a Contributor License Agreement should be made available at some point in time. Until then, please contact us at [opensource@olvid.io](mailto:opensource@olvid.io) if you would like to contribute.

If you face issues with these tools please write us at [bot@olvid.io](mailto:bot@olvid.io).
We are also very interested in knowing how you use these tools and what kind of bots you develop, especially if you try to use our daemon with another client language. Please do not hesitate to get in touch with us 😁, we will be glad to hear from you.

# License
The Olvid bot framework is licensed under the GNU Affero General Public License v3. The full license is available in [`LICENSE`](./LICENSE).

```
Olvid
Copyright © 2019-2024 Olvid SAS

Olvid is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License, version 3,
as published by the Free Software Foundation.

Olvid is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Olvid.  If not, see <https://www.gnu.org/licenses/>.
```
