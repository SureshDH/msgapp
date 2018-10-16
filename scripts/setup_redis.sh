#!/bin/bash

install_redis_depends(){

    sudo apt install curl -y

    sudo apt-get install tcl8.5 -y
}

install_redis(){

    install_redis_depends

    curl -O http://download.redis.io/redis-stable.tar.gz

    tar -xvf redis-stable.tar.gz

    cd redis-stable

    make

    make test

    sudo  make install

}

make_confs(){
    # Configure redis confs

    sudo mkdir /etc/redis

    sudo cp redis.conf /etc/redis

    # sudo nano /etc/redis/redis.conf

    sudo sed -i 's/^supervised no/supervised systemd/g' /etc/redis/redis.conf

    sudo sed -i 's/dir .\//dir \/var\/lib\/redis/g' /etc/redis/redis.conf
}

prepare_redis_service(){
    # Creates redis daemon service file

    echo  '
    # add
    [Unit]
    Description=Redis In-Memory Data Store
    After=network.target

    [Service]
    User=redis
    Group=redis
    ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
    ExecStop=/usr/local/bin/redis-cli shutdown
    Restart=always

    [Install]
    WantedBy=multi-user.targeti' | sudo tee  /etc/systemd/system/redis.service > /dev/null

    sudo adduser --system --group --no-create-home redis

    sudo mkdir /var/lib/redis

    sudo chown redis:redis /var/lib/redis

    sudo chmod 770 /var/lib/redis


}

start_resis(){

    # starts the redis service
    sudo systemctl start redis

    sudo systemctl status redis --no-pager
}

install_redis
make_confs
prepare_redis_service
start_resis
