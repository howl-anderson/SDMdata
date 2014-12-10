#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json


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

    req = requests.Session()
    r = req.get(url, params=args)
    r.raise_for_status()

    string_data = r.content
    original_data = json.loads(string_data)

    return original_data


if __name__ == "__main__":
    data = species_match(name='Petrocephalus catostoma catostoma')
    print data