#!/usr/bin/env bash

function start {
    echo "🚀 Starting all services..."
    docker-compose up --build
}

function stop {
    echo "🛑 Stopping all services..."
    docker-compose down
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac