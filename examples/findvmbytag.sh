#!/usr/bin/env bash
#
# Find all virtual machines with a given tag or optionally 
# tag/value 
#
# Usage: findvmbytag <tagname> [tagval]
#

tag="$1"
if [ "$2" ]
then
    tagval="=='$2'"
else
    tagval=""
fi

jmespath="[?tags.${tag}${tagval}]"
az vm list-all --query "${jmespath}"
