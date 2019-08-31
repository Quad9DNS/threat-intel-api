# threat-hit-api
This repository contains sample code for threat intelligence providers who provide Quad9 with a threat intel feed. Contact Quad9 (support@quad9.net) for a valid API Key.

# Overview

threat-intel-api is an HTTP/Websocket service that allows threat intelligence (TI) providers to retrieve telemetry data generated from the malicious domain names they provide to Quad9 via their threat intelligence feeds. 

Contact Quad9 at support@quad9.net if you are a threat intelligence provider and need a key. 

If a client has multiple threat lists they will be given a separate token for each list.


# Starting a Session
Clients initiate their session by making an HTTP GET request to the service. There is only one endpoint: "/". In this initial request, the client is expected to provide a "bearer" token in the `Authorization`header, like so:

`HTTP/``1.1`  `GET /`

`Authorization: Token <THE_ACTUAL_TOKEN>`

When the client supplies a valid, active token, their connection will be "upgraded" to a Websocket.

## API Business Rules

threat-intel-api was written with the following business rules in place:

-   Clients must acknowledge each message they receive;
-   Clients must acknowledge messages in the order they are received within 5 seconds. (This can be adjusted with a config setting)
-   Multiple clients connecting with the same authorization token is allowed and increases throughput;

If a client fails to acknowledge the messages they receive, in-order, the API will terminate the connection.

# Python Example

The example script tia_example.py was written against Python version 3.6.
Convenient way to setup a 3.6 environment on Linux. https://linuxize.com/post/how-to-install-python-3-on-centos-7/


