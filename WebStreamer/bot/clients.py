# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import asyncio
import logging
from os import environ
from ..vars import Var
from WebStreamer.utils.config_parser import TokenParser
from pyrogram import Client
from . import multi_clients, work_loads, sessions_dir, StreamBot

logger = logging.getLogger("multi_client")

async def initialize_clients():
    multi_clients[0] = StreamBot
    work_loads[0] = 0
    all_tokens = TokenParser().parse_from_env()
    if not all_tokens:
        logger.info("No additional clients found, using default client")
        return
    
    async def start_client(client_id, token):
        try:
            logger.info(f"Starting - Client {client_id}")
            if client_id == len(all_tokens):
                await asyncio.sleep(2)
                print("This will take some time, please wait...")
            client = await Client(
                name=str(client_id),
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                bot_token=token,
                sleep_threshold=Var.SLEEP_THRESHOLD,
                workdir=sessions_dir if Var.USE_SESSION_FILE else Client.PARENT_DIR,
                no_updates=True,
                in_memory=not Var.USE_SESSION_FILE,
            ).start()
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logger.error(f"Failed starting Client - {client_id} Error:", exc_info=True)
    
    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])
    multi_clients.update(dict(clients))
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True
        logger.info("Multi-client mode enabled")
    else:
        logger.info("No additional clients were initialized, using default client")
