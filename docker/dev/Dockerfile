#
#  Development Dockerfile for justpy
#
# Created by Wolfgang Fahl 2022-08-21
# see
# https://github.com/elimintz/justpy/issues/434

# Start with a python environment
FROM python:3.10-slim

LABEL maintainer="Wolfgang Fahl - wf@bitplan.com"

# working directory
WORKDIR /usr/src/

# install justpy, green and pandas
RUN pip install --no-cache-dir justpy

# Development stuff
# install git
RUN apt update
RUN apt install -y git nano vim

RUN git clone https://github.com/elimintz/justpy

# pip install green testing environment
# https://pypi.org/project/green/
RUN pip install green
# install requirements for demo browser
RUN pip install pandas bokeh matplotlib plotly pydeck pygments seaborn vega_datasets pydevd
