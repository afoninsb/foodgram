#!/bin/sh
sudo docker stop $(sudo docker ps -a -q)
sudo docker-compose up -d
