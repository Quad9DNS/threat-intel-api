#!/usr/bin/env python

import asyncio
import websockets
import json
import sys
import os
import time
import argparse

#
# Connect to the Quad9 threat-intel api and receive domain block information
# You receive the auth_token from Quad9 and it is specific to a threat feed.
#
# Requires Python version 3.6 or greater
#
# usage:
#     ./tia_example.py  --auth_token <YOUR TOKEN>
#         This measures download speed
#
#     ./tia_example.py  --verbose  --auth_token <YOUR TOKEN>
#         To see the data being retrieved.



async def readblockloop():
    async with websockets.connect(args.connect_url,
            extra_headers={'Authorization': Token "YOUR TOKEN" + args.auth_token}) as ws:


        global websocket
        count = 0
        start = time.perf_counter()

        websocket = ws

        while True:
            try:
                message = await websocket.recv()
                #print(f" {message}")
                data = json.loads(message)
                if args.verbose:
                    print(f" {data}")

                # We do our processing here. Just a count
                count = count + 1
                if (count % 10000 == 0):
                    end = time.perf_counter()
                    print(f' {count} {count/(end-start)}/sec')

                ack = dict(id=data['id'])

                if not args.noack:
                    await acks.put(ack)
                #print(f" acks: {acks}")
            except:
                print('Failed to receive message')
                break


async def process_acks():
    while True:
        ack = await acks.get()

        try:
            await send_data(ack)
        except:
            print('Failed to send ack')
            break


async def send_data(data):
    frame = json.dumps(data)
    await websocket.send(frame)

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Read from Quad9 threat-intel api')

    parser.add_argument('--verbose', action='store_true',
                        help='Dump out received json')

    parser.add_argument('--noack', action='store_true',
                        help='Disable acks so no data is confirmed read. Primarily for testing')

    # Optional arguments
    parser.add_argument('--auth_token', default="Token <YOUR TOKEN>",
                        help='Authorization token from quad9 to access the api')

    parser.add_argument('--connect_url', default='wss://tiapi.quad9.net',
                        help='url to access the api')


    global args
    args = parser.parse_args()



    tasks = [
        asyncio.ensure_future(readblockloop()),
        asyncio.ensure_future(process_acks()),
    ]

    global acks
    acks = asyncio.Queue()

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
