#!/usr/bin/env python
# -*- coding:utf-8-*-

import requests
import requests.exceptions
import json
import logging
from logging.handlers import RotatingFileHandler
import Exceptions


logger = logging.getLogger('species_match')
logger.setLevel(logging.DEBUG)

log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'log', 'species_search.log')
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def species_search(q=None,
                   rank=None,
                   highertaxon_key=None,
                   status=None,
                   extinct=None,
                   habitat=None,
                   name_type=None,
                   dataset_key=None,
                   nomenclatural_status=None,
                   limit=20,
                   facet=None,
                   facet_only=None,
                   facet_mincount=None,
                   facet_multiselect=None,
                   type=None):

    url = 'http://api.gbif.org/v1/species/search'

    args = {"q": q,
            "rank": rank,
            "highertaxonKey": highertaxon_key,
            "status": status,
            "isExtinct": extinct,
            "habitat": habitat,
            "nameType": name_type,
            "datasetKey": dataset_key,
            "nomenclatural_status": nomenclatural_status,
            "limit": limit,
            "facet": facet,
            "facet_only": facet_only,
            "facet_mincount": facet_mincount,
            "facet_multiselect": facet_multiselect,
            "type": type}

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
    data = species_search(q="mammalia")