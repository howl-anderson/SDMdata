#!/usr/bin/env python

import csv
import os
from osgeo import ogr
import osgeo.osr as osr
from db import Occurrence
from db import create_session


def export_data(target_dir, output_format="csv", country_list=None, output_type=None):
    session = create_session()
    species_list = session.query(Occurrence.species_name).distinct(Occurrence.species_name).filter(
        Occurrence.cross_check == 1).all()
    for species in species_list:
        species_name = species.species_name
        if country_list is None:
            if output_type is None:
                occurrence_data_set = session.query(Occurrence).filter(Occurrence.species_name == species_name).all()
            else:
                occurrence_data_set = session.query(Occurrence).filter(Occurrence.species_name == species_name,
                                                                       Occurrence.cross_check.in_(output_type)).all()

        else:
            if output_type is None:
                occurrence_data_set = session.query(Occurrence).filter(Occurrence.species_name == species_name,
                                                                       Occurrence.country_code.in_(country_list)).all()
            else:
                occurrence_data_set = session.query(Occurrence).filter(Occurrence.species_name == species_name,
                                                                       Occurrence.country_code.in_(country_list),
                                                                       Occurrence.cross_check.in_(output_type)).all()
        if output_format == "csv":
            output_file = os.path.join(target_dir, species_name + ".csv")
            fd = open(output_file, "wb")
            csv_writer = csv.writer(fd)
            for occurrence_point in occurrence_data_set:
                longitude = occurrence_point.longitude
                latitude = occurrence_point.latitude
                csv_writer.writerow([longitude, latitude, occurrence_point.cross_check])
            fd.close()
        elif output_format == "shp":
            output_dir = os.path.join(target_dir, species_name)
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)

            # create the data source
            output_file = os.path.join(output_dir, "presence.shp")

            driver = ogr.GetDriverByName("ESRI Shapefile")

            data_source = driver.CreateDataSource(output_file)

            # create the spatial reference, WGS84
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)

            # create the layer
            layer = data_source.CreateLayer("main", srs, ogr.wkbPoint)

            # Add the fields we're interested in
            field_name = ogr.FieldDefn("Species", ogr.OFTString)
            field_name.SetWidth(24)
            layer.CreateField(field_name)

            field_name = ogr.FieldDefn("Country", ogr.OFTString)
            field_name.SetWidth(24)
            layer.CreateField(field_name)

            field_name = ogr.FieldDefn("CrossCheck", ogr.OFTInteger)
            layer.CreateField(field_name)

            # multipoint = ogr.Geometry(ogr.wkbMultiPoint)

            for occurrence_point in occurrence_data_set:
                longitude = occurrence_point.longitude
                latitude = occurrence_point.latitude
                # point = (longitude, latitude)
                # point_object = ogr.Geometry(ogr.wkbPoint)
                # point_object.AddPoint(*point)
                # multipoint.AddGeometry(point_object)

                feature = ogr.Feature(layer.GetLayerDefn())
                # Set the attributes using the values from the delimited text file
                print str(occurrence_point.species_name)
                feature.SetField("Species", str(occurrence_point.species_name))
                feature.SetField("Country", str(occurrence_point.country_code))

                if occurrence_point.cross_check is None:
                    # TODO: In case of cross check is not finished
                    cross_check = -3
                else:
                    cross_check = int(occurrence_point.cross_check)
                feature.SetField("CrossCheck", cross_check)

                # Create the WKT for the feature using python string formatting
                wkt = "POINT(%f %f)" % (float(longitude), float(latitude))

                # Create the point from the Well Know Txt
                point = ogr.CreateGeometryFromWkt(wkt)

                # Set the feature geometry using the point
                feature.SetGeometry(point)
                # Create the feature in the layer (shapefile)
                layer.CreateFeature(feature)
                # Destroy the feature to free resources
                feature.Destroy()

            data_source.Destroy()