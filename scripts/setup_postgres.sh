#!/bin/bash

install_postgres(){
    sudo apt install python-pip -y
    sudo apt install wget -y

    sudo apt-get update

    sudo apt-get install -y postgresql postgresql-contrib

    sudo service postgresql status

}

setup_conf(){
    sudo sed -e 's/local   all             postgres                                peer/local   all             postgres                                md5/g' /etc/postgresql/10/main/pg_hba.conf
}

restart_postgres(){

    sudo service postgresql restart
    sudo service postgresql status --no-pager

}

populate_schema(){

    wget https://gist.githubusercontent.com/paragradke/a629bb4e332125b1388390fcc156cfcd/raw/1a1e3b62e847a60e89f9c84d016e11f057c672bb/schema.sql

    sudo -u postgres createdb auzmore

    sudo -u postgres psql auzmore -c "ALTER USER postgres with password 'root123'";

    echo  "Enter password for postgres as root123"
    sudo psql -U postgres auzmore < schema.sql


}

install_postgres
populate_schema
setup_conf
restart_postgres

