import argparse
from .pull import pull


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--branch", type=str, help="Branch", required=False, default=None
    )
    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        help="Destination",
        required=False,
        default="prompts.json",
    )
    parser.add_argument(
        "-t", "--token", type=str, help="API token", required=False, default=None
    )
    parser.add_argument(
        "--_env", type=str, help=argparse.SUPPRESS, required=False, default="prod"
    )
    parser.add_argument(
        "--_dry", type=bool, help=argparse.SUPPRESS, required=False, default=False
    )

    args = parser.parse_args()
    pull(
        branch=args.branch,
        destination=args.destination,
        api_token=args.token,
        _dry=args._dry,
        _env=args._env,
    )


if __name__ == "__main__":
    raise SystemExit(main())
