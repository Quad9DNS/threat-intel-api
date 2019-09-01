# threat-hit-api
This repository contains sample code for threat intelligence providers who provide Quad9 with a threat intel feed. Contact Quad9 (support@quad9.net) for a valid API Key.

# Overview

threat-intel-api is an HTTP/Websocket service that allows threat intelligence (TI) providers to retrieve telemetry data generated from the malicious domain names they provide to Quad9 via their threat intelligence feeds. 

Contact Quad9 at support@quad9.net if you are a threat intelligence provider and need a key. 

Clients will access the api via a websocket.
Clients need the url of the websocket (https://tiapi.quad9.net) and an authorization token.

If a client has multiple threat lists they will be given a separate token for each list.

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

# Simple Curl Example

curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" -H "Sec-WebSocket-Version: 13" -H "Authorization: Token <YOUR TOKEN>"  https://tiapi.quad9.net >> output.txt

If it is working you will see output like:
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 14940    0 14940    0     0   1867      0 --:--:--  0:00:08 --:--:--     0

Sends to a file called output.txt 

Exmple single entry:

{"id":"6004","qname":"blockeddomain.example.com","qtype":"TXT","timestamp":"2019-05-24T06:29:18.843081648Z","city":"AQ","region":"AQ","country":"AQ"}

id = unique id for a single record 
qname = domain that the user queried for
qtype = type of DNS record 
timestamp = time/date of the query 
city = city that the query originated from (or closest with the minimum population), can be blank
region = region that the query originated from, an be blank
country = two character country code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)that the query originated from, can be blank

Note: We use MaxMind for geographic lookups but we snap locations to the center of the closest city that is above the minimum population - it never moves out of a region (typically a country or nation) but you will not get granular geographic information for small cities. This is to ensure end user privacy.



# Python Example

The example script tia_example.py was written against Python version 3.6.
Convenient way to setup a 3.6 environment on Linux. https://linuxize.com/post/how-to-install-python-3-on-centos-7/

 This measures download speed:


(my_project_venv) [exampleuser@commandline]$  ./tia_example.py    --auth_token <YOUR TOKEN> 
 10000 8140.593486210115/sec
 20000 9139.962665341003/sec
 30000 9979.32015085066/sec
 40000 10866.962743213264/sec
 50000 10731.540519453485/sec
 
 To see the data being retrieved:
 
 (my_project_venv) [exampleuser@commandline]$  ./tia_example.py    --auth_token <YOUR TOKEN>  --verbose
 {'id': '191960005', 'qname': 'blockeddomain.example.com', 'qtype': 'A', 'timestamp': '2018-12-11T03:15:47.038932839Z', 'city': 'San Jose', 'region': 'CA', 'country': 'US'}
 {'id': '191961005', 'qname': 'blockeddomain.example.com', 'qtype': 'A', 'timestamp': '2018-12-11T03:15:47.051392978Z', 'city': 'San Jose', 'region': 'CA', 'country': 'US'}
 {'id': '191962005', 'qname': 'blockeddomain.example.com', 'qtype': 'A', 'timestamp': '2018-12-11T03:15:47.0605273Z', 'city': 'San Jose', 'region': 'CA', 'country': 'US'}
 {'id': '191963005', 'qname': 'blockeddomain.example.com', 'qtype': 'A', 'timestamp': '2018-12-11T03:15:47.102118471Z', 'city': 'San Jose', 'region': 'CA', 'country': 'US'}

#Usage

Clients must acknowledge that messages have been received.

In the example above the script will send back to the server json objects of {"id":'191960005'} to indicate that is has successfully received and processed the json structure.

If the websocket is termininated before the ack is received by the server the message will be resent on the next connection.
