#!/usr/bin/env python3
import os
import typing as t
from argparse import ArgumentParser
from argparse import Namespace

from dotenv import find_dotenv
from dotenv import load_dotenv
from slack_sdk import WebClient


def _main(args: t.List[str]) -> int:
    parsed = _parse_args(args)
    dotenv_file = find_dotenv(".holler.env")
    print(dotenv_file)
    load_dotenv(dotenv_file)
    token = os.environ.get("TOKEN")
    client = WebClient(token=token)
    channel_id = _get_channel_id(channel="host-status", client=client)
    kwargs = parsed.__dict__
    kwargs.update({"text": " ".join(kwargs["text"])})
    kwargs.update({"channel": channel_id})
    client.chat_postMessage(**kwargs)
    return 0


def _get_channel_id(channel: str, client: WebClient) -> str:
    channels = client.conversations_list()
    for channel_info in channels.data["channels"]:
        if channel_info["name"] == channel:
            return channel_info["id"]

    raise ValueError(f"Channel {channel} not found")


def _parse_args(args: t.List[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "text", metavar="MESSAGE", type=str, nargs="*", help="Message to post"
    )
    parser.add_argument("-c", "--channel", help="The channel to post in", required=True)
    parser.add_argument(
        "-u", "--username", help="Custom username to write the message as"
    )
    parser.add_argument("-b", "--blocks", help="The message block(s) to post")
    parsed = parser.parse_args(args)
    return parsed


def _cli():
    import sys

    sys.exit(_main(sys.argv[1:]))
