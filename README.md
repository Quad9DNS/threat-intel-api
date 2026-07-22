# threat-intel-api

This repository contains sample code for threat intelligence providers who provide Quad9 with a threat intel feed consisting of domains that are malicious and which are subsequently blocked by Quad9's blocking-capable service address sets. Partners should contact Quad9 (support@quad9.net) for a valid API Key.

# Overview

threat-intel-api is an HTTP/Websocket service that allows threat intelligence (TI) providers to retrieve telemetry data generated from the malicious domain names they provide to Quad9 via their threat intelligence feeds. This is for TI providers who have signed agreements with Quad9 to supply threat data (domains) - it is not a general API for Quad9.

Contact Quad9 at support@quad9.net if you are a threat intelligence provider and need a key. 

Client software will access the API via a websocket. If a client has multiple threat lists they will be given separate and URLs for each list with the same authentication credentials.


## Requirements
Clients need:
- the URL of the websocket (https://tiapi.quad9.net/<URL PATH PROVIDED BY QUAD9 PER PROVIDER LIST>)
- authentication credentials (username/password) supplied by Quad9
- a streaming websocket client or client library that supports TLS-encrypted websocket feeds (wss:)


## API Business Rules

threat-intel-api was written with the following business rules in place:

- event data is transmitted only to TI providers who supplied the specific domain names in the events
- multiple TI providers may supply an identical domain name; each will get an independent copy of the event data
- data is delivered in JSON format
- data is streamed in near-realtime (typically less than 5 seconds from end-to-end)
- events are queued in a ring buffer, up to 100000 events in the buffer. If the client disconnects, it is possible to pick back up without message loss as long as no more than 100000 events have transpired since disconnect and the reconnection includes the last successfully received message-id.
- clients may connect without specifying a "last-seen" item, and the newest events and onwards will be delivered




# Simple wsget example

Python,  Go, Rust, and most other languages have websocket libraries for more advanced API connections. Using the "wscat" (https://github.com/websockets/wscat) open source connection tool it is possible to perform simple tests to validate feed status. Other options for command-line websocket connect are tools like websocat (https://github.com/vi/websocat) or curl 8.14.0+ onwards. 

Example:

```
wscat --auth yoyodyne-labs:UeBX9mXEpq33Mu3 --connect "wss://tapi4.quad9.net/tiapi/yoyodyne-KCWk7HRP3AR/"
```

If it is working the command will generate output like:

```
Connected (press CTRL+C to quit)
< {"blockedNameData":{"addressesV4":{"answers":[{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"178.63.248.53","recordType":"A","recordTypeId":1,"ttl":126},{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"157.90.33.78","recordType":"A","recordTypeId":1,"ttl":126},{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"157.90.33.79","recordType":"A","recordTypeId":1,"ttl":126},{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"178.63.248.50","recordType":"A","recordTypeId":1,"ttl":126},{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"178.63.248.55","recordType":"A","recordTypeId":1,"ttl":126},{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"178.63.248.54","recordType":"A","recordTypeId":1,"ttl":126},{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"178.63.248.48","recordType":"A","recordTypeId":1,"ttl":126},{"asn":{"autonomous_system_number":24940,"autonomous_system_organization":"HETZNER ONLINE G.M.B.H."},"class":"IN","domainName":"one-new-message-okay.com","geoip":{"city":{"names":{"en":"Auerbach"}},"country":{"iso_code":"DE"},"location":{"latitude":50.51,"longitude":12.4},"subdivisions":[{"iso_code":"13"}],"traits":{"autonomous_system_number":24940,"autonomous_system_organization":"Hetzner Online GmbH","user_type":"hosting"}},"rData":"178.63.248.49","recordType":"A","recordTypeId":1,"ttl":126}]},"dataAge":256,"nameservers":{"answers":[{"class":"IN","domainName":"one-new-message-okay.com","rData":"aspen.ns.cloudflare.com.","recordType":"NS","recordTypeId":2,"ttl":9631},{"class":"IN","domainName":"one-new-message-okay.com","rData":"braden.ns.cloudflare.com.","recordType":"NS","recordTypeId":2,"ttl":9631}],"dataAge":1784564933}},"geoip":{"city":{"names":{"en":"Jakarta"}},"country":{"iso_code":"ID"},"location":{"latitude":-6.21,"longitude":106.84},"subdivisions":[{"iso_code":"04"}],"traits":{"autonomous_system_number":139428,"autonomous_system_organization":"PT.LEXXA DATA INDONUSA","user_type":"residential"}},"messageType":"ClientQuery","message_id":"019f805b-e990-73b3-b4dd-9f7cf5b601ba","pop_code":"jkt","requestData":{"fullRcode":0,"header":{"aa":false,"ad":true,"anCount":0,"arCount":1,"cd":false,"id":0,"nsCount":0,"opcode":0,"qdCount":1,"qr":0,"ra":false,"rcode":0,"rd":true,"tc":false},"opt":{"do":true,"ednsVersion":0,"extendedRcode":0,"udpPayloadSize":8192},"question":[{"class":"IN","domainName":"one-new-message-okay.com.","etld":{"etld":"com.","etld_plus":"one-new-message-okay.com.","known_suffix":true,"tld":"com."},"questionType":"A","questionTypeId":1}],"rcodeName":"NoError"},"responseAddress":"9.9.9.9","responsePort":853,"serverId":"res130.jkt","socketFamily":"INET","socketProtocol":"DOT","timestamp":"2026-07-20T16:28:53.284Z"}
```

Example single entry (parsed through "jq -r" for readability)

```json
{
  "blockedNameData": {
    "addressesV4": {
      "answers": [
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "178.63.248.53",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        },
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "157.90.33.78",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        },
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "157.90.33.79",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        },
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "178.63.248.50",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        },
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "178.63.248.55",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        },
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "178.63.248.54",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        },
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "178.63.248.48",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        },
        {
          "asn": {
            "autonomous_system_number": 24940,
            "autonomous_system_organization": "HETZNER ONLINE G.M.B.H."
          },
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "geoip": {
            "city": {
              "names": {
                "en": "Auerbach"
              }
            },
            "country": {
              "iso_code": "DE"
            },
            "location": {
              "latitude": 50.51,
              "longitude": 12.4
            },
            "subdivisions": [
              {
                "iso_code": "13"
              }
            ],
            "traits": {
              "autonomous_system_number": 24940,
              "autonomous_system_organization": "Hetzner Online GmbH",
              "user_type": "hosting"
            }
          },
          "rData": "178.63.248.49",
          "recordType": "A",
          "recordTypeId": 1,
          "ttl": 126
        }
      ]
    },
    "dataAge": 256,
    "nameservers": {
      "answers": [
        {
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "rData": "aspen.ns.cloudflare.com.",
          "recordType": "NS",
          "recordTypeId": 2,
          "ttl": 9631
        },
        {
          "class": "IN",
          "domainName": "one-new-message-okay.com",
          "rData": "braden.ns.cloudflare.com.",
          "recordType": "NS",
          "recordTypeId": 2,
          "ttl": 9631
        }
      ],
      "dataAge": 1784564933
    }
  },
  "geoip": {
    "city": {
      "names": {
        "en": "Jakarta"
      }
    },
    "country": {
      "iso_code": "ID"
    },
    "location": {
      "latitude": -6.21,
      "longitude": 106.84
    },
    "subdivisions": [
      {
        "iso_code": "04"
      }
    ],
    "traits": {
      "autonomous_system_number": 139428,
      "autonomous_system_organization": "PT.LEXXA DATA INDONUSA",
      "user_type": "residential"
    }
  },
  "messageType": "ClientQuery",
  "message_id": "019f805b-e990-73b3-b4dd-9f7cf5b601ba",
  "pop_code": "jkt",
  "requestData": {
    "header": {
      "aa": false,
      "ad": true,
      "anCount": 0,
      "arCount": 1,
      "cd": false,
      "id": 0,
      "nsCount": 0,
      "opcode": 0,
      "qdCount": 1,
      "qr": 0,
      "ra": false,
      "rcode": 0,
      "rd": true,
      "tc": false
    },
    "opt": {
      "do": true,
      "ednsVersion": 0,
      "extendedRcode": 0,
      "udpPayloadSize": 8192
    },
    "question": [
      {
        "class": "IN",
        "domainName": "one-new-message-okay.com.",
        "etld": {
          "etld": "com.",
          "etld_plus": "one-new-message-okay.com.",
          "known_suffix": true,
          "tld": "com."
        },
        "questionType": "A",
        "questionTypeId": 1
      }
    ]
  },
  "responseAddress": "9.9.9.9",
  "responsePort": 853,
  "serverId": "res130.jkt",
  "socketFamily": "INET",
  "socketProtocol": "DOT",
  "timestamp": "2026-07-20T16:28:53.284Z"
}
```

Generally, Quad9 supplies information about individual DNS lookup events which have been blocked in a way that preserves privacy but gives threat intelligence providers insight into the malicious activity that has been prevented.

This data comprises: blurred information about the victim, detailed information about the malicious targets, and meta-information about the event stream. NO PII OF CLIENTS IS INCLUDED OR REFERENCED, AND NO CLIENT IP ADDRESS DATA IS EVER INCLUDED.  All IP addresses above are target IP addresses - the outcome of DNS lookups to the A or AAAA records of malicious domains.  See Quad9's privacy policy which governs the data transmitted by Quad9 in these and all telemetry aggregations: https://quad9.net/privacy/policy/

Not all lookups are for A or AAAA results.  Some lookups are for NS, TXT, or other results. These records will have varying degrees of additional information per what is available for that particular record type.

Data fields, brief summary:

- `pop_code` = POP from which the query was sourced. See www.quad9.net/locations for POP names, but generally three-letter IATA codes are embedded in the POP name.
- `socketProtocol` = DOT, DOH, UDP, TCP, DOQ and others may appear as standards emerge
- `responsePort` = which port was used for the inbound connection
- `responseAddress` = to which Quad9 service address was the client sending the query
- `requestData` = DNS request information
- `geoip` = blurred geographic, network, and demographic data about client (victim.)  Currently, only English names are supplied for place names.
- `blockedNameData` = the IPv4, IPv6 addresses of the blocked lookup, and nameservers of the blocked lookup. This is what would have been delivered to the victim if the query had been permitted.
- `message_id` = the sequence number in this websocket stream.

*_Note: We have multiple sources for geographic data, but we snap/blur locations to the center of the closest city that is above the minimum population - it never moves out of a region (typically a country or nation) but you will not get granular geographic information for small cities. This is to ensure end user privacy. Target data uses the same geographic database._*

## Disconnection and reconnection

To ensure full delivery of all messages, you may wish to keep state on the "message_id" record. This identifier changes with each subsequent message.  It allows the data feed to pick up where it left off on next connection using the "last_received" parameter in the wss URL.

Example:

``` 
wscat --auth yoyodyne-labs:UeBX9mXEpq33Mu3 --connect "wss://tapi4.quad9.net/tiapi/yoyodyne-KCWk7HRP3AR?last_received=019f805b-e990-73b3-b4dd-9f7cf5b601ba"
```

Websockets may be disconnected by client libraries if there is insufficient traffic - make sure to set a ping interval of less than 20 seconds. Quad9 does not disconnect sessions due to inactivity, but client libraries may have that configured as a default. Ensure that if there is a disconnection that your client re-connects immediately.

If the message-id pointer specified has expired from the queue, your websocket connection will start transmitting the oldest items in the ring buffer first.

Multiple clients connecting on the same authentication and URL criteria may create unexpected duplications, though this is untested in detail. Please use a single socket connection. 

Sockets are easily capable of transmitting tens of thousands of events per second if there are that volume of blocks happening within your threat data set; please ensure you have adequate buffering on the receiver side.

v2027/07/21.01 jtodd
