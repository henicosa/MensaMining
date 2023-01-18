#!/bin/bash
docker volume create mensamining_log
docker volume create mensamining_data
docker build ./ -t mensamining
docker run -p 5105:5000 -v mensamining_log:/app/log -v mensamining_data:/app/raw mensamining