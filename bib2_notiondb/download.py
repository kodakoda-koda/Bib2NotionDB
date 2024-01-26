from bib2_notiondb.notion_api import get_bibtex_string_list_from_database
from bib2_notiondb.utilities import write_to_file


def download(
    file_path: str,
    cite_in: str,
    token: str,
    database_id: str,
) -> int:
    """Write the bibliography from the database `database_id` in the file
    located at `file_path`.

    Args:
        file_path: File path in which the bibliography will be saved.
        cite_in: Which paper to download.
        token: Notion API token.
        database_id: Targeted database id.

    Returns:
        Error code.
    """
    bibtex_str_list = get_bibtex_string_list_from_database(
        cite_in=cite_in,
        token=token,
        database_id=database_id,
    )
    write_to_file(
        content="\n\n".join(bibtex_str_list),
        file_path=file_path,
    )
    return 0
