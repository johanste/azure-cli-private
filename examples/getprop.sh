#!/usr/bin/env bash

grep "$1" | cut -d':' -f2 | sed 's/ //g'