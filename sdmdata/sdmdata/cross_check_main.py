#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from osgeo import ogr

from iso3166 import countries
from db import Occurrence
from db import create_session


def cross_check(work_dir="."):
    session = create_session()
    feature_dir = {}

    base_dir = os.path.join(work_dir, 'gadm')
    dir_name_list = [o for o in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, o))]

    for dir_name in dir_name_list:
        # dir_name = "USA_adm"
        feature_name = dir_name.split("_")[0]
        shape_file = os.path.join(base_dir, dir_name + "/" + dir_name + "0.shp")
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = driver.Open(shape_file, 0)
        layer = dataSource.GetLayer()

        feature = layer[0]
        feature_dir[feature_name] = feature

    occurrence_list = session.query(Occurrence).filter(Occurrence.cross_check == None).all()
    correct_record = []
    wrong_record = []
    country_wrong_record = []

    for item in occurrence_list:
        oid = item.id
        longitude = item.longitude
        latitude = item.latitude
        country_code = item.country_code
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(longitude, latitude)

        # Create polygon
        try:
            country_data = countries.get(country_code)
            country_code = country_data[2]
            poly = feature_dir[country_code]
            poly = poly.geometry()
        except KeyError:
            # print(country_code + " don't exists")
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": -1},
                                                                          synchronize_session=False)
            session.commit()
            country_wrong_record.append(oid)
            continue

        intersection = poly.Intersects(point)
        # print(intersection)
        if intersection:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": 1}, synchronize_session=False)
            session.commit()
            correct_record.append(oid)
        else:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": 0}, synchronize_session=False)
            session.commit()
            wrong_record.append(oid)

    session.close()
    return correct_record, wrong_record, country_wrong_record