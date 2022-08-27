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

# use working copy of JustPy instead of the latest pypi version to also be able to test branches and non-released code
ADD justpy /usr/local/lib/python3.10/site-packages/justpy

# provide a simple example as a default
COPY docker/main.py .

ENV HOST 0.0.0.0

CMD /usr/local/bin/python main.py
