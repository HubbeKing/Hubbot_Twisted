#!/bin/bash

REPO=registry.hubbe.club/hubbot

buildah bud -t $REPO:latest .
buildah push $REPO:latest
