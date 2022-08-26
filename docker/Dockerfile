#
#  Dockerfile for justpy
#
# Created by Wolfgang Fahl 2022-08-21
# see
# https://github.com/elimintz/justpy/issues/434

# Start with a python environment
FROM python:3.10-slim

LABEL maintainer="Wolfgang Fahl - wf@bitplan.com"

# working directory
WORKDIR /usr/src/

# install justpy
RUN pip install --no-cache-dir justpy
