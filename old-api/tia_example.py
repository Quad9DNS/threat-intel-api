#!/usr/bin/env python

#
# Connect to the Quad9 threat-intel api and receive domain block information
# You receive the auth_token from Quad9 and it is specific to a threat feed.
#
# Requires Python version 3.8 or greater.
#
# usage:
#     ./tia_example.py --config <YOUR CONFIG FILE>
#
# set verbose: true to see the data being retrieved.

# @author: Emilia Cebrat-Maslowski (Quad9)

import os
import logging 
import asyncio
import websockets
import json
import yaml
import sys
import os
import time
import argparse

from aiofile import async_open
from collections import namedtuple


def read_config(config_path):
    with open(config_path, 'r') as f:
          parsed_file = yaml.safe_load(f)
    Config = namedtuple("Config", "ti_url auth_token data_file log_file verbose nolog noack")
    config = Config(
 		parsed_file['ti_url'], 
		parsed_file['auth_token'], 
		parsed_file['data_file'],
		parsed_file['log_file'],
		parsed_file['verbose'], 
		parsed_file['nolog'], 
		parsed_file['noack']
	     )
    return config


async def readblockloop(config, events):
   
    async with websockets.connect(config.ti_url,
            extra_headers={'Authorization': "Token " + config.auth_token}) as ws:

        global websocket
        websocket = ws

        while True:
            try:
                message = await websocket.recv()
                if config.verbose:
                    print(f" {message}")

                if not config.nolog:
                    await events.put(message)
            except:
                logging.debug('Failed to receive message')
                await asyncio.sleep(1)


async def process_acks(acks):
    while True:
        ack = await acks.get()

        try:
            logging.debug(f"ACKing: {ack}")
            await send_data(ack)
        except:
            logging.debug('Failed to send ack')
            break


async def send_data(data):
    frame = json.dumps(data)
    await websocket.send(frame)

async def process_events(config, events, acks):
    while True:
        async with async_open(config.data_file, "a") as f:
            event = await events.get()
            await f.write(event)
            if not config.noack:
                event_parsed = json.loads(event)
                ack = dict(id=event_parsed['id'])
                await acks.put(ack)


def main():

    parser = argparse.ArgumentParser(description='Read from Quad9 threat-intel api')
    parser.add_argument('--config', required=True, 
                        help='Path to the config file.')
    args = parser.parse_args()
    config = read_config(args.config)
    logging.basicConfig(filename=config.log_file, level=logging.INFO, format='%(message)s')
    loop = asyncio.get_event_loop()
    acks = asyncio.Queue()
    events = asyncio.Queue()

    try:
        loop.create_task(readblockloop(config, events))
        loop.create_task(process_events(config, events, acks))
        loop.create_task(process_acks(acks))
        loop.run_forever()
    finally:
        loop.close()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
