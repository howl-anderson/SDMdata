#!/usr/bin/env python

from iso3166 import countries
from osgeo import ogr
from db import Occurrence
from db import create_session
import os
import Queue
import signal
import sys


def signal_handler(self, signal, frame):
    print('Received signal to exit!')
    sys.exit(0)


def worker(queue, work_dir):
    # register signal process function
    signal.signal(signal.SIGTERM, signal_handler)

    session = create_session()
    feature_dict = {}

    base_dir = os.path.join(work_dir, 'gadm')
    dir_name_list = [o for o in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, o))]

    for dir_name in dir_name_list:
        feature_name = dir_name.split("_")[0]
        shape_file = os.path.join(base_dir, dir_name + "/" + dir_name + "0.shp")
        driver = ogr.GetDriverByName("ESRI Shapefile")
        data_source = driver.Open(shape_file, 0)
        layer = data_source.GetLayer()

        feature = layer[0]
        feature_dict[feature_name] = feature

    while True:
        try:
            oid, longitude, latitude, country_code = queue.get(True, 1000)
        except Queue.Empty:
            break
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(longitude, latitude)

        if country_code is None:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": -3},
                                                                          synchronize_session=False)
            session.commit()
            continue
        elif country_code in countries:
            country_data_alpha_3 = countries.get(country_code)[2]
            if country_data_alpha_3 in feature_dict.keys():
                poly = feature_dict[country_data_alpha_3]
                poly = poly.geometry()
            else:
                session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": -1},
                                                                              synchronize_session=False)
                session.commit()
                return None
        else:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": -2},
                                                                          synchronize_session=False)
            session.commit()
            return None

        intersection = poly.Intersects(point)

        if intersection:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": 1}, synchronize_session=False)
            session.commit()
        else:
            session.query(Occurrence).filter(Occurrence.id == oid).update({"cross_check": 0}, synchronize_session=False)
            session.commit()

    return None