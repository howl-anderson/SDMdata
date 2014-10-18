#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from osgeo import ogr


from iso3166 import countries
from db import Occurrence
from db import create_session

# TODO: write this to other gdal script
ogr.UseExceptions()


def cross_check(work_dir="."):
    session = create_session()
    feature_dir = {}

    base_dir = os.path.join(work_dir, 'gadm')
    dir_name_list = [o for o in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, o))]

    for dir_name in dir_name_list:
        feature_name = dir_name.split("_")[0]
        shape_file = os.path.join(base_dir, dir_name + "/" + dir_name + "0.shp")
        driver = ogr.GetDriverByName("ESRI Shapefile")
        data_source = driver.Open(shape_file, 0)
        layer = data_source.GetLayer()

        feature = layer[0]
        feature_dir[feature_name] = feature

    occurrence_list = session.query(Occurrence).filter(Occurrence.cross_check == None).all()

    for item in occurrence_list:
        oid = item.id
        longitude = item.longitude
        latitude = item.latitude
        country_code = item.country_code
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(longitude, latitude)

        if country_code is None:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": -3},
                                                                          synchronize_session=False)
            session.commit()
            continue
        elif country_code in countries:
            country_data_alpha_3 = countries.get(country_code)[2]
            if country_data_alpha_3 in feature_dir.keys():
                poly = feature_dir[country_data_alpha_3]
                poly = poly.geometry()
            else:
                session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": -1},
                                                                              synchronize_session=False)
                session.commit()
                continue
        else:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": -2},
                                                                          synchronize_session=False)
            session.commit()
            continue

        intersection = poly.Intersects(point)

        # print(intersection)
        if intersection:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": 1}, synchronize_session=False)
            session.commit()
        else:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": 0}, synchronize_session=False)
            session.commit()

    session.close()
    return None