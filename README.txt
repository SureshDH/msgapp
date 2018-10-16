The sample messaging app. Which uses flask framework to create the
micro service. Which handles the post requests from the clients and
validates them.

Setup bringup:
===============
msgapp
├── scripts
    ├── setup_postgres.sh
    ├── setup_redis.sh

    Under scripts directory execute `bash setup_postgres.sh` and
`bash setup_redis.sh` to build the setup. Which installs the postgres server
and redis server. Along with their depndencies. Gets schema.sql and creates a
db named `auzmore`. Also populates the schema.sql into the `auzmore` database
to create `account` and `phone_number` relations.

Installation:
============
    Run `pip install --upgrade -r requirements.txt` to install the requirements.
    Also run `bash app_service.sh`, this will make the service as daemon.
    Inside `msgapp` repository run `sudo python setup.py install`. This will
install the msgapp either under site or dist packages. This installation also
starts the app. Which will be running in the background.

Tests:
======
msgapp
├── tests
    ├── integration
        ├── client.py
    └── unit
        ├── test_app.py

    For unit testcases install `sudo apt install python-pytest -y`

    Both integration and unit tests covers different testcases. Can run
`python client.py` to test the integration test and run `py.test` in the `unit`
directory to test the unit test cases.


Run app:
========
    Once the installation gets completed. Run `msgapp`. This will run the server.


Note:
====
    As of now the unit testcases doesn't mock either redis or postgres
database servers. So it requires that the db servers should be running while
testing the unit tests.

    All the coding and testing has done on Ubuntu 18.04(4.15.0-36-generic)

