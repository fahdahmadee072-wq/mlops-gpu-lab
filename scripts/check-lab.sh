#!/usr/bin/env bash
echo "== Distro:            $WSL_DISTRO_NAME"
echo "== Bad mounts (want none):"; awk 'NF != 6' /proc/mounts
echo "== Docker engine:     $(docker info --format '{{.OperatingSystem}}')"
echo "== Docker mirrors:    $(docker info --format '{{.RegistryConfig.Mirrors}}')"
echo "== Registry:          $(docker ps --filter name=local-registry --format '{{.Status}}')"
echo "== Registry images:   $(curl -s http://localhost:5000/v2/_catalog)"
echo "== k3s service:       $(systemctl is-active k3s)"
sudo k3s kubectl get nodes
sudo k3s kubectl get pods -A
echo "== GPU on node:"; sudo k3s kubectl describe node | grep -m2 'nvidia.com/gpu'
