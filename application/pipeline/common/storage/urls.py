"""
This module has a number of public methods which are useful for
verifying and cleaning URLs.
"""
# import logging
import re
import requests
from urllib.parse import urlparse
from functools import lru_cache
import tldextract

# logger = logging.getLogger(__name__)


def validate_url_string(url_string):
    """
    Determines whether the given `url_string` is a valid URL with an https
    scheme.
    If not, attempts to mangle the URL scheme into the desired form,
    falling back to an http scheme in the event TLS is not supported.
    If all attempts to save the input string fail, returns None
    Required Arguments:
    url_string:  URL (string) which will be validated and/or repaired.
    """
    # logger.debug(f'Validating_url {url_string}')
    if not type(url_string) == str or not url_string:
        return
    else:
        upgraded_url = _add_best_scheme(url_string)

    parse_result = urlparse(upgraded_url)
    tld = tldextract.extract(upgraded_url)
    #
    # logger.debug(f'parse_result.scheme: {parse_result.scheme}')
    # logger.debug(f'tld.domain: {tld.domain}')
    # logger.debug(f'tld.suffix: {tld.suffix}')

    if tld.domain and tld.suffix and parse_result.scheme:
        return upgraded_url
    elif tld.ipv4 and parse_result.scheme:
        # logger.debug(f'Using IP address as URL: {upgraded_url}')
        return upgraded_url
    else:
        # logger.info(
        #     f'Invalid url {url_string}, attempted upgrade: {upgraded_url}.'
        #     ' Returning None'
        # )
        return None
def add_url_scheme(url_string, scheme='http'):
    """
    Replaces the scheme of `url_string` with `scheme`,
    or adds the given `scheme` if necessary.
    """
    # logger.debug(f'Adding or changing scheme of {url_string} to {scheme}')
    stripped_url = url_string.strip()
    scheme_pattern = re.compile('https*:/*')
    scheme_match = scheme_pattern.match(stripped_url)
    if scheme_match is not None:
        url_no_scheme = stripped_url[scheme_match.end():].strip('/')
    else:
        url_no_scheme = stripped_url.strip('/')
    url_with_scheme = f'{scheme}://{url_no_scheme}'
    # logger.debug(f'URL with scheme: {url_with_scheme}')
    return url_with_scheme


def _add_best_scheme(url_string):
    domain_key = tldextract.extract(url_string).fqdn
    if not domain_key:
        domain_key = tldextract.extract(url_string).ipv4

    if _test_domain_for_tls_support(domain_key):
        upgraded_url = add_url_scheme(url_string, scheme='https')
    else:
        upgraded_url = add_url_scheme(url_string, scheme='http')

    return upgraded_url


@lru_cache(maxsize=1024)
def _test_domain_for_tls_support(domain):
    # logger.info(f'Testing {domain} for TLS support')
    tls_supported = False
    try:
        requests.get(f'https://{domain}', timeout=2)
        # logger.info(f'{domain} supports TLS.')
        tls_supported = True
    except Exception as e:
        pass
        # logger.info(
        #     f'Could not verify TLS support for {domain}. Error was\n{e}'
        # )
    return tls_supported
