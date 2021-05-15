from common import requester
from common.storage import dtm

DELAY = 2
REQUEST_TYPE = 'books'
ENDPOINT = f'http://gutendex.com/{REQUEST_TYPE}'
PROVIDER = 'projectgutenberg'
PROVIDER_SITE = 'http:gutendex.com'
COLLECTION_SITE = 'https://www.gutenberg.org/'
DEFAULT_QUERY_PARAMS = {}

delayed_requester = requester.DelayedRequester(DELAY)
dtm_store = dtm.DtmStore(provider=PROVIDER)


def main():
    dtm_list = get_dtm_list()
    _ = _process_dtm_list(dtm_list)

    return dtm_store.total_dtm_entities


def get_dtm_list(
        endpoint=ENDPOINT,
        retries=5
):
    dtm_list = []
    page = 2038
    cond = True
    while cond:
        query_params = _build_query_param(page=page)
        page += 1
        json_response_in_pydict_form = delayed_requester.get_response_json(
            endpoint=endpoint,
            retries=retries,
            query_params=query_params
        )

        # extract results array
        results = _extract_results_array_from_json(json_response_in_pydict_form)

        if results is None:
            break
        # Insert dtm entities from results array into book_list
        for dtm_entity in results:
            dtm_list.append(dtm_entity)
        print(page, len(dtm_list))
        if json_response_in_pydict_form.get("next") is None:
            cond = False


    if len(dtm_list) == 0:
        return None
    else:
        print(len(dtm_list))
        return dtm_list


def _build_query_param(
        default_query_params=DEFAULT_QUERY_PARAMS,
        page=1
):
    query_params = default_query_params.copy()
    query_params.update(
        {
            'page': page
        }
    )

    return query_params


def _extract_results_array_from_json(json_response_in_pydict_form):
    if (
            json_response_in_pydict_form is None
            or json_response_in_pydict_form.get("results") is None
            or len(json_response_in_pydict_form.get("results")) == 0
    ):
        results = None
    else:
        results = json_response_in_pydict_form.get("results")

    return results


def _process_dtm_list(dtm_list):
    total_dtm_entities = 0
    if dtm_list is not None:
        for dtm_entity in dtm_list:
            total_dtm_entities = _process_dtm_entity(dtm_entity)

    return total_dtm_entities


def _process_dtm_entity(dtm_entity):
    id = dtm_entity.get("id")
    title = dtm_entity.get("title")
    author = get_authors(dtm_entity)
    languages = dtm_entity.get("languages")
    download_links = get_download_links(dtm_entity)
    copyright = dtm_entity.get("copyright")

    foreign_landing_url = f'{COLLECTION_SITE}ebooks/{id}'
    provider_site = PROVIDER_SITE


    return dtm_store.add_item(
            id=id,
            title=title,
            author=author,
            languages=languages,
            download_links=download_links,
            copyright=copyright,
            foreign_landing_url=foreign_landing_url,
            provider_site=provider_site
    )

def get_authors(dtm_entity):
    authors = None
    _authors = dtm_entity.get("authors")

    if len(_authors) != 0:
        authors = _authors[0].get("name")

    return authors

def get_download_links(dtm_entity):

    download_links = None
    download_links_dict = {k: v for k, v in dtm_entity.get("formats").items() if v is not None}
    _download_link = list(download_links_dict.values())
    download_link = _download_link[0]

    return download_link

if __name__ == "__main__":
    main()
