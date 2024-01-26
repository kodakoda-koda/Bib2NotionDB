from typing import List, Optional

from bibtexparser.bibdatabase import BibDatabase

from bib2_notiondb.bibtex import (
    get_bib_database_from_file,
    get_bib_database_from_string,
    get_publication_list,
)
from bib2_notiondb.notion_api import (
    add_publications_to_database,
    get_publication_key_list_from_database,
)
from bib2_notiondb.publication import Publication
from bib2_notiondb.utilities import NotionScholarException


class IllegalArgumentException(NotionScholarException):
    pass


def run(
    token: str,
    database_id: str,
    bib_file_path: Optional[str] = None,
    bib_string: Optional[str] = None,
) -> int:
    if bib_string is not None:
        bib_database: BibDatabase = get_bib_database_from_string(string=bib_string)

    elif bib_file_path is not None:
        bib_database = get_bib_database_from_file(file_path=bib_file_path)

    else:
        raise IllegalArgumentException('Must provide a "string" or a "file_path"')

    publication_list: List[Publication] = get_publication_list(bib_database)
    key_list = get_publication_key_list_from_database(
        token=token,
        database_id=database_id,
    )

    publication_list_filtered = [p for p in publication_list if p.key not in key_list]  # noqa: E501
    add_publications_to_database(
        publications=publication_list_filtered,
        token=token,
        database_id=database_id,
    )

    if not publication_list_filtered and publication_list:
        print("\nAll the publications are already present in the database.")

    return 0
