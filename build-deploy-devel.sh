#!/bin/bash -ex
[ -z $1 ] && echo need version tag - devel will be added automatically && exit 2
VER=${1}-devel
prom_vars=$(grep "Gauge(" monitor/prometheus.py | awk '{print $1}')
for v in $prom_vars
do
    sed "s/$v/devel_$v/g" -i monitor/*.py
done

docker build . -t <YOUR_REPO>/tools/monitor:$VER
#revert
for v in $prom_vars
do
    sed "s/devel_$v/$v/g" -i monitor/*.py
done

docker push <YOUR_REPO>/tools/monitor:$VER
helm upgrade --install -f helm/values.yaml --set version=$VER --set image.tag=$VER monitor helm/  --create-namespace --namespace tools-monitor-devel --debug