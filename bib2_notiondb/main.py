import argparse
import sys

from bib2_notiondb.config import ConfigManager
from bib2_notiondb.download import download
from bib2_notiondb.run import run
from bib2_notiondb.utilities import get_token


def get_parser():
    token = get_token()
    config = ConfigManager().get()

    # Parent parser
    parent_parser = argparse.ArgumentParser(add_help=False)

    parser = argparse.ArgumentParser(
        description="bib2notiondb",
        usage=f'Use "bib2notiondb --help" or "bn --help" for more information. \n',  # noqa: E501
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Choice of the subparser
    subparsers = parser.add_subparsers(
        help="Selection of the action to perform.",
        dest="mode",
    )

    # Run parser
    run_parser = subparsers.add_parser(
        "run",
        parents=[parent_parser],
        help="Run bib2notiondb.",
    )
    run_parser.add_argument(
        "-t",
        "--token",
        default=None,
        type=str,
        metavar="",
        required=token is None,
        help=f"Token used to connect to Notion. \n(default: {token})",
    )
    run_parser.add_argument(
        "-db",
        "--database-id",
        default=None,
        type=str,
        metavar="",
        help=f"Database that will be furnished. The database_id can be found in the url of the database: \n"
        f"https://www.notion.so/{{workspace_name}}/{{database_id}}?v={{view_id}} \n"
        f'(default: {config.get("database_id", None)})',
    )

    if config.get("file_path", None) is None:
        group = run_parser.add_mutually_exclusive_group(required=True)
    else:
        group = run_parser.add_argument_group()

    group.add_argument(
        "-f",
        "--file-path",
        default=None,
        type=str,
        metavar="",
        help=f"Bib file that will be used. This argument is required if the bib file is not saved in the config and no bib-string is passed. \n"
        f'(default: {config.get("bib_file_path", None)})',  # noqa: E501
    )
    group.add_argument(
        "-s",
        "--string",
        default=None,
        type=str,
        metavar="",
        help='Bibtex entries to add (must be in-between three quotes """<bib-string>"""). '
        "By default, the entries will be saved to the bib file from the config. "
        'It is possible to disable this behavior by changing the "save" option: "bn setup -save false".',
    )

    # Download bibtex parser
    download_parser = subparsers.add_parser(
        "download",
        parents=[parent_parser],
        help="Download the bibtex entries present in the notion database.",
    )
    download_parser.add_argument(
        "-f",
        "--file-path",
        default=None,
        type=str,
        metavar="",
        required=True,
        help="File in which the bibtex entries will be saved.",
    )
    download_parser.add_argument(
        "-c", "--cite_in", default=None, type=str, metavar="", required=True, help="Which paper to download."
    )
    download_parser.add_argument(
        "-t",
        "--token",
        default=None,
        type=str,
        metavar="",
        required=token is None,
        help=f"Token used to connect to Notion. \n(default: {token})",
    )
    download_parser.add_argument(
        "-db",
        "--database-id",
        default=None,
        type=str,
        metavar="",
        help=f"Database that will be downloaded. The database_id can be found in the url of the database: \n"
        f"https://www.notion.so/{{workspace_name}}/{{database_id}}?v={{view_id}} \n"
        f'(default: {config.get("database_id", None)})',
    )

    # Clear config parser
    clear_parser = subparsers.add_parser(  # noqa: F841
        "clear-config",
        parents=[parent_parser],
        help="Clear the bib2notiondb config.",
    )

    # Inspect config parser
    inspect_parser = subparsers.add_parser(  # noqa: F841
        "inspect-config",
        parents=[parent_parser],
        help="Inspect the bib2notiondb config.",
    )

    # Setup parser
    setup_parser = subparsers.add_parser(
        "set-config",
        parents=[parent_parser],
        help="Save the provided preferences.",
    )
    setup_parser.add_argument(
        "-f",
        "--file-path",
        default=None,
        type=str,
        metavar="",
        help=f"Save the bibtex file that will be used when running bib2notiondb without source arguments. "
        f"The path must be absolute and the file need to exist. "
        f'(current: {config.get("bib_file_path", None)})',
    )
    setup_parser.add_argument(
        "-t",
        "--token",
        default=None,
        type=str,
        metavar="",
        help=f"Save the Notion integration token. \n(current: {token})",
    )
    setup_parser.add_argument(
        "-db",
        "--database-id",
        default=None,
        type=str,
        metavar="",
        help=f"Save the database-id in the user config. "
        f"The database_id can be found in the url of the database: \n"
        f"https://www.notion.so/{{workspace_name}}/{{database_id}}?v={{view_id}} \n"
        f'(current: {config.get("database_id", None)})',
    )

    return parser


def main() -> int:
    parser = get_parser()
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    kwargs = vars(arguments)
    mode = kwargs.pop("mode", None)
    config_manager = ConfigManager(**kwargs)

    if mode == "run":
        return run(**config_manager.get_run_kwargs())

    elif mode == "download":
        return download(**config_manager.get_download_kwargs())

    elif mode == "set-config":
        config_manager.setup()
        return 0

    elif mode == "inspect-config":
        config_manager.inspect()
        return 0

    elif mode == "clear-config":
        config_manager.clear()
        return 0

    else:
        raise NotImplementedError("Invalid mode.")
