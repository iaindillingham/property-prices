#!/usr/bin/env bash

DST_DIR=reports/figures

# https://medium.com/@adamhooper/fonts-in-node-canvas-bbf0b6b0cabf
PANGOCAIRO_BACKEND=fontconfig

mkdir -p $DST_DIR
vg2png -b models/ --format specs/format.json specs/map.vg.json $DST_DIR/map.png
vg2pdf -b models/ --format specs/format.json specs/map.vg.json $DST_DIR/map.pdf
