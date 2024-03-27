#!/bin/bash -ex
VER=$1
[ -z $VER ] && echo need version tag && exit 2
docker build . -t <YOUR_REPO>/tools/monitor:$VER
docker push <YOUR_REPO>/tools/monitor:$VER
helm upgrade --install -f helm/values.yaml --set version=$VER --set image.tag=$VER monitor helm/  --create-namespace --namespace tools-monitor