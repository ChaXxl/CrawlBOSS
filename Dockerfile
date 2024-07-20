FROM ubuntu:latest
LABEL authors="xxl"

ENTRYPOINT ["top", "-b"]