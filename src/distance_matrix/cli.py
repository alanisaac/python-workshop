import argparse


def _get_arg_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input", nargs=1)
    arg_parser.add_argument("asyncio", action='store_true')
    return arg_parser


def get_args() -> argparse.Namespace:
    arg_parser = _get_arg_parser()
    args = arg_parser.parse_args()
    return args
