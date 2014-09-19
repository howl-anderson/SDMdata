#!/usr/bin/env python
#-*- coding:utf-8 -*-

import click
from sdmdata.cross_check_main import cross_check


def main():
    correct_record, wrong_record, country_wrong_record = cross_check()
    click.echo("Number of correct record: %s" % len(correct_record))
    click.echo("Number of wrong record: %s" % len(wrong_record))
    click.echo("Number of record that have wrong/unkown country code: %s" % len(country_wrong_record))

if __name__ == "__main__":
    main()