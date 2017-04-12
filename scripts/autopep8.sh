#!/bin/bash

LIBFILES="$(find ./lif_ethernet -name '*.py' | tr '\n' ' ')"

autopep8 -ia --ignore=E501 ${LIBFILES}
