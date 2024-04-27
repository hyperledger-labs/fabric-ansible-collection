#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#
from urllib.parse import urlparse, urlunparse


def translate_url_to_os_format(source_url, type):

    translated_url = source_url

    parsedURL = urlparse(source_url)

    if parsedURL.port != 443:

        parsedHostname = parsedURL.hostname.split(".")

        parsedHostname[0] = parsedHostname[0] + '-' + type

        hostname = ".".join(parsedHostname)

        urlTuple = (hostname, '443')

        netloc = ":".join(urlTuple)

        newPasrsedURL = parsedURL._replace(netloc=netloc)

        translated_url = urlunparse(newPasrsedURL)

    return translated_url
