from collections import namedtuple
from datetime import datetime
from dotenv import load_dotenv
import os
from common.storage import column


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.normpath(os.path.join(CURRENT_DIR,'..','..','..','..','config'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

_DTM_TSV_COLUMNS = [
    # The order of this list maps to the order of the columns in the TSV.
    column.StringColumn(
        name='id', required=True, size=3000, truncate=True
    ),
    column.StringColumn(
        name='title', required=True, size=3000, truncate=True
    ),
    column.StringColumn(
        name='author', required=False, size=3000, truncate=True
    ),
    column.StringColumn(
        name='languages', required=False, size=3000, truncate=True
    ),
    column.JSONColumn(
        name='download_links', required=False
    ),
    column.BooleanColumn(
        name='copyright', required=False
    ),
    column.URLColumn(
        name='foreign_landing_url', required=True, size=3000
    ),
    column.StringColumn(
        name='provider_site', required=False, size=2000, truncate=True
    )
]

DTM_entity = namedtuple(
    'DTM_entity',
    [c.NAME for c in _DTM_TSV_COLUMNS]
)


class DtmStore:
    """
    A class that stores information about a DTM entity from a given provider.
    provider:       String marking the provider in the record table of the DB.
    output_file:    String giving a temporary .tsv filename (*not* the
                    full path) where the info should be stored.
    output_dir:     String giving a path where `output_file` should be placed.
    buffer_length:  Integer giving the maximum number of entity information rows
                    to store in memory before writing them to disk.
    """

    def __init__(
            self,
            provider=None,
            output_file=None,
            output_dir=None,
            buffer_length=50
    ):
        self._entity_buffer = []
        self._total_dtm_entities = 0
        self._PROVIDER = provider
        self._BUFFER_LENGTH = buffer_length
        self._NOW = datetime.now()
        self._OUTPUT_PATH = self._initialize_output_path(
            output_dir,
            output_file,
            provider,
        )

    def add_item(
            self,
            id=None,
            title=None,
            author=None,
            languages=None,
            download_links=None,
            copyright=None,
            foreign_landing_url=None,
            provider_site=None
    ):
        entity = DTM_entity(
                id=id,
                title=title,
                author=author,
                languages=languages,
                download_links=download_links,
                copyright=copyright,
                foreign_landing_url=foreign_landing_url,
                provider_site=provider_site
        )

        tsv_row = self._create_tsv_row(entity)
        # print(tsv_row)
        if tsv_row:
            self._entity_buffer.append(tsv_row)
            self._total_dtm_entities += 1

        if len(self._entity_buffer) >= self._BUFFER_LENGTH:
            self._flush_buffer()

        return self._total_dtm_entities

    def commit(self):
        """Writes all remaining entities in the buffer to disk."""
        self._flush_buffer()

        return self._total_dtm_entities

    def _initialize_output_path(self, output_dir, output_file, provider):
        if output_dir is None:
            output_dir = os.getenv('OUTPUT_DIR')
        if output_dir is None:
            output_dir = '/tmp'

        if output_file is not None:
            output_file = str(output_file)
        else:
            output_file = (
                f'{provider}_{datetime.strftime(self._NOW, "%Y%m%d%H%M%S")}'
                f'.tsv'
            )

        output_path = os.path.join(output_dir, output_file)
        return output_path

    def _get_total_dtm_entities(self):
        return self._total_dtm_entities

    """Get total images for directly using in scripts."""
    total_dtm_entities = property(_get_total_dtm_entities)

    def _create_tsv_row(
            self,
            entity,
            columns=_DTM_TSV_COLUMNS
    ):
        row_length = len(columns)
        prepared_strings = [
            columns[i].prepare_string(entity[i]) for i in range(row_length)
        ]

        for i in range(row_length):
            if columns[i].REQUIRED and prepared_strings[i] is None:
                return None
            else:
                return '\t\t'.join(
                    [s if s is not None else '\\N' for s in prepared_strings]
                ) + '\n'

    def _flush_buffer(self):
        buffer_length = len(self._entity_buffer)
        if buffer_length > 0:
            with open(self._OUTPUT_PATH, 'a') as f:
                f.writelines(self._entity_buffer)
                self._entity_buffer = []
        else:
            pass
        return buffer_length
