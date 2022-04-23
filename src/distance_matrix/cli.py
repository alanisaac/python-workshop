import argparse
from enum import Enum


class Runner(Enum):
    STANDARD = 'standard'
    ASYNCIO = 'asyncio'
    PANDAS = 'pandas'

    def __str__(self):
        return self.value


def _get_arg_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input", nargs=1)
    arg_parser.add_argument(
        "-r", "--runner", type=Runner, choices=list(Runner), default=Runner.STANDARD
    )
    return arg_parser


def get_args() -> argparse.Namespace:
    arg_parser = _get_arg_parser()
    args = arg_parser.parse_args()
    return args
