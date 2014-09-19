#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import json
import pprint
import requests
# import pdb


class OccurrenceSearch:
    api_url = 'http://api.gbif.org/v1/occurrence/search'
    page_size = 300
    query_args = None
    record_count = None
    page_start_point = 0
    original_data = None
    results = None
    proxy = None
    timeout = 60

    def __init__(self, proxy=None, timeout=None):
        self.proxy = proxy
        if timeout is not None:
            self.timeout = timeout

        self.pp = pprint.PrettyPrinter(indent=4)

    def search(self,
               taxon_key=None,
               scientific_name=None,
               country=None,
               publishing_country=None,
               has_coordinate=None,
               type_status=None,
               record_number=None,
               last_interpreted=None,
               continent=None,
               geometry=None,
               collector_name=None,
               basis_of_record=None,
               dataset_key=None,
               event_date=None,
               catalog_number=None,
               year=None,
               month=None,
               decimal_latitude=None,
               decimal_longitude=None,
               elevation=None,
               depth=None,
               institution_code=None,
               collection_code=None,
               spatial_issues=None,
               search=None):
        query_args = {"taxon_key": taxon_key,
                      "scientific_name": scientific_name,
                      "country": country,
                      "publishing_country": publishing_country,
                      "has_coordinate": has_coordinate,
                      "type_status": type_status,
                      "record_number": record_number,
                      "last_interpreted": last_interpreted,
                      "continent": continent,
                      "geometry": geometry,
                      "collector_name": collector_name,
                      "basis_of_record": basis_of_record,
                      "dataset_key": dataset_key,
                      "event_date": event_date,
                      "catalog_number": catalog_number,
                      "year": year,
                      "month": month,
                      "decimal_latitude": decimal_latitude,
                      "decimal_longitude": decimal_longitude,
                      "elevation": elevation,
                      "depth": depth,
                      "institution_code": institution_code,
                      "collection_code": collection_code,
                      "spatial_issues": spatial_issues,
                      "search": search}
        self.query_args = query_args
        meta_query_args = query_args
        meta_query_args["limit"] = 1

        original_data = self.web_interface(**meta_query_args)
        self.record_count = original_data["count"]

        self.fetch_record()
        record_matrix = self.collect_record()
        return record_matrix

    def fetch_record(self, start=0):
        limit = self.page_size
        this_query_args = self.query_args
        this_query_args["start"] = start
        this_query_args["limit"] = limit
        original_data = self.web_interface(**this_query_args)
        results = original_data["results"]
        if self.results is None:
            self.results = results
        else:
            self.results.extend(results)

        # ready to start new loop
        start_point = start + limit
        if start_point <= self.record_count:
            self.fetch_record(start=start_point)

    def web_interface(self,
                      taxon_key=None,
                      scientific_name=None,
                      country=None,
                      publishing_country=None,
                      has_coordinate=None,
                      type_status=None,
                      record_number=None,
                      last_interpreted=None,
                      continent=None,
                      geometry=None,
                      collector_name=None,
                      basis_of_record=None,
                      dataset_key=None,
                      event_date=None,
                      catalog_number=None,
                      year=None,
                      month=None,
                      decimal_latitude=None,
                      decimal_longitude=None,
                      elevation=None,
                      depth=None,
                      institution_code=None,
                      collection_code=None,
                      spatial_issues=None,
                      search=None,
                      limit=20,
                      start=None):


        args = {"taxonKey": taxon_key,
                "scientificName": scientific_name,
                "country": country,
                "publishingCountry": publishing_country,
                "hasCoordinate": has_coordinate,
                "typeStatus": type_status,
                "recordNumber": record_number,
                "lastInterpreted": last_interpreted,
                "continent": continent,
                "geometry": geometry,
                "collectorName": collector_name,
                "basisOfRecord": basis_of_record,
                "datasetKey": dataset_key,
                "eventDate": event_date,
                "catalogNumber": catalog_number,
                "year": year,
                "month": month,
                "decimalLatitude": decimal_latitude,
                "decimalLongitude": decimal_longitude,
                "elevation": elevation,
                "depth": depth,
                "institutionCode": institution_code,
                "collectionCode": collection_code,
                "spatialIssues": spatial_issues,
                "q": search,
                "limit": limit,
                "offset": start}

        url = self.api_url
        # try:
        #     # pp.pprint(args)
        #     if self.proxy is None:
        #         r = requests.get(url, params=args, timeout=self.timeout)
        #         r.raise_for_status()
        #     else:
        #         r = requests.get(url, params=args, timeout=self.timeout, proxies=self.proxy)
        #         r.raise_for_status()
        #         # self.pp.pprint(r.url)
        # except requests.exceptions.Timeout, e:
        #     print e
        #     sys.exit()

        if self.proxy is None:
            r = requests.get(url, params=args, timeout=self.timeout)
            r.raise_for_status()
        else:
            r = requests.get(url, params=args, timeout=self.timeout, proxies=self.proxy)
            r.raise_for_status()

        # pp.pprint(self.query_args)
        # pp.pprint(args)
        # pp.pprint(r.url)
        # sys.exit()
        string_data = r.content
        try:
            original_data = json.loads(string_data)
            return original_data
        except:
            print(string_data)
            sys.exit()

    def collect_record(self):
        data_list = self.results
        # pdb.set_trace()
        record_list = [(item["decimalLongitude"], item["decimalLatitude"], item["countryCode"])
                       for item in data_list
                       if ("decimalLongitude" in item.keys()) & ("decimalLatitude" in item.keys())]
        # pp.pprint(record_list)
        no_record_list = [item
                          for item in data_list
                          if ("decimalLongitude" not in item.keys()) or ("decimalLatitude" not in item.keys())]
        return record_list, no_record_list


if __name__ == "__main__":
    obj = OccurrenceSearch()
    data, _ = obj.search(taxon_key=2435099)
    # pp.pprint(data)
    #proxies = {
    #    'http': 'http://127.0.0.1:8087',
    #    'https': 'http://127.0.0.1:8087',
    #}
