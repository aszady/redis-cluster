#!/bin/bash

sleep 1

nodes=()
for IP in $(dig "redis" +short); do
  nodes+=("$IP:6379")
done
echo "${nodes[@]}"

redis-cli --cluster create \
  "${nodes[@]}" \
  --cluster-replicas 1 \
  --cluster-yes
echo "🚀 Redis cluster ready."