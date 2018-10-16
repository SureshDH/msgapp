#!/bin/bash


echo  '
# add
[Unit]
Description=Mesage application
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/msgapp
Restart=always

[Install]
WantedBy=multi-user.targeti' | sudo tee  /etc/systemd/system/msgapp.service > /dev/null
