# This is a Dockerfile for creating a Thug https://github.com/buffer/thug Container from the latest
# honeynet/thug image. The difference between the base image is that this instance will try to connect
# to a MongoDB database running on the docker host: this is needed for Project Rumal's backend.
# More on Rumal here:
# - https://github.com/pdelsante/rumal
# - https://github.com/reachtarunhere/rumal
#
FROM honeynet/thug
MAINTAINER pietro.delsante@gmail.com

RUN sed -i s/localhost/`/sbin/ip route|awk '/default/ { print  $3}'`/g /opt/thug/src/Logging/logging.conf
