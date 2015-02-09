#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import requests
import requests.exceptions
import json
import logging
from logging.handlers import RotatingFileHandler
import Exceptions


logger = logging.getLogger('species_match')
logger.setLevel(logging.DEBUG)

log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'log', 'species_match.log')
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def species_match(name,
                  rank=None,
                  kingdom=None,
                  phylum=None,
                  clazz=None,
                  order=None,
                  family=None,
                  genus=None,
                  strict=False,
                  verbose=False,
                  start=None,
                  limit=20):
    url = 'http://api.gbif.org/v1/species/match'
    args = {"name": name,
            "rank": rank,
            "kingdom": kingdom,
            "phylum": phylum,
            "clazz": clazz,
            "order": order,
            "family": family,
            "genus": genus,
            "strict": strict,
            "verbose": verbose,
            "offset": start,
            "limit": limit}

    try:
        req = requests.Session()
        r = req.get(url, params=args)
        r.raise_for_status()
        string_data = r.content
        original_data = json.loads(string_data)

        return original_data
    except requests.exceptions.RequestException as e:
        logger.error('Network error!')
        raise Exceptions.NetworkError(str(e))


if __name__ == "__main__":
    data = species_match(name='Petrocephalus catostoma catostoma')
    print data