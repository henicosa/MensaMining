#!/bin/bash
docker run -p 5105:5000 -v mensamining_log:/app/log -v mensamining_data:/app/raw mensamining