#!/bin/bash

echo "--- 💥 STARTING CHAOS SELF-HEALING DEMO 💥 ---"
echo "Current Pod Status:"
kubectl get pods -l app=target-app

echo ""
echo "🔥 KILLING the Juice Shop Application..."
# Delete the specific pod. Kubernetes Deployment will notice and restart it,.
kubectl delete pod -l app=target-app

echo ""
echo "🚑 Watching for Self-Healing (Ctrl+C to stop)..."
# Watch the pods restart in real-time
kubectl get pods -l app=target-app -w