#!/usr/bin/env python
#-*- coding:utf-8 -*-
# TODO: this function design for CLI, may removed later

import click
import csv
from sdmdata.collect_record_main import collect_record_data


def main():
    species_not_exists_list, species_no_record_list, species_no_data_list = collect_record_data()
    species_not_exists_count = len(species_not_exists_list)
    species_no_record_count = len(species_no_record_list)
    species_no_data_count = len(species_no_data_list)

    click.echo("Number of species name not exists in GBIF: %s" % species_not_exists_count)
    if species_not_exists_count:
        fd = open("species_name_not_exists_in_gbif.csv", "wb")
        csv_writer = csv.writer(fd, delimiter=',', quotechar='"')
        for species_name in species_not_exists_list:
            csv_writer.writerow([species_name])
        fd.close()
        click.echo(">>> Species name that not exists in GBIF are list in file: species_name_not_exists_in_gbif.csv")

    click.echo("Number of species that don't have coordinate occurrence points: %s" % species_no_record_count)
    if species_no_record_count:
        fd = open("species_have_no_coordinate_occurrence.csv", "wb")
        csv_writer = csv.writer(fd, delimiter=',', quotechar='"')
        for species_name in species_no_record_list:
            csv_writer.writerow([species_name])
        fd.close()
        click.echo(">>> Species that don't have coordinate occurrence points are list in file: species_have_no_coordinate_occurrence.csv")

    click.echo("Number of species that have un-coordinate occurrence points: %s" % species_no_data_count)
    if species_no_data_count:
        fd = open("species_have_un_coordinate_occurrence.csv", "wb")
        csv_writer = csv.writer(fd, delimiter=',', quotechar='"')
        for species_name in species_no_data_list.keys():
            csv_writer.writerow([species_name])
        fd.close()
        click.echo(">>> Species that have un-coordinate occurrence points are list in file: species_have_no_coordinate_occurrence.csv")

if __name__ == "__main__":
    main()