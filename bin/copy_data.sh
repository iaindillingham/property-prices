#!/usr/bin/env bash

DST_DIR=models/data

mkdir -p $DST_DIR
cp data/processed/aggregated_price_paid_data/aggregated-pp-2019.csv $DST_DIR
cp data/processed/bdline_gb/district_borough_unitary.json $DST_DIR
