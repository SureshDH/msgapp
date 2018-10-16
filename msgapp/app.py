#!/usr/bin/python

import json
import redis
import time
import threading
import os
import sys

import psycopg2

from msgapp import constants


from flask import Flask, request, session, jsonify


# app = Flask(__name__)
lock = threading.Lock()

database = "auzmore"
user = "postgres"
password = "root123"
host = "localhost"
port = "5432"

ps = ""
rs = ""

class PostgresSQLServer(object):
    """This class implements the db related operations for
       postgressql db.
    """

    def __init__(self):
        """Open postgressql db connection  """

        self.db_conn = psycopg2.connect(database = database, user = user,
                                password = password, host = host, port = port)

        self.db_cur = self.db_conn.cursor()

    def fireQuery(self, query):
        """ Executes the query and return the output. """

        self.db_cur.execute(query)
        return self.db_cur.fetchall();


class RedisServer(object):
    """This class implements redis in memory related operations ."""
    def __init__(self):
        """ Open a connection with redis db.  """
        self.redis_conn = redis.Redis('localhost')



def verify_services():
    """Before starting the app, veifies whether the postgres or
    redis are running. Otherwise exit.
    """

    try:
        ps = PostgresSQLServer()
        rs = RedisServer()
        rs.redis_conn.ping()
        return ps, rs
    except :
        return None, None

def timeout():
    """Delets all the keys and values after 24 hours  ."""    

    rs = RedisServer()
    
    while True:
        lcounter = rs.redis_conn.get("limit_counter")
        # limit_counter becomes zero after 24 hours
        if not lcounter:
            lock.acquire()
            while rs.redis_conn.scard("lcounter") > 0:
                rs.redis_conn.spop("lcounter")
            lock.release()
        time.sleep(2)

def messageApplication():
    """ This class initiates the flask server. """

    app = Flask(__name__)
    app.config['ps'] = PostgresSQLServer()
    app.config['rs'] = RedisServer()
 
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    rs = app.config['rs']
    ps = app.config['ps']


    def validateParamas(_from, to, text):
        """Validate the input params. """

        length = ""
        err_msg = "%s is invalid"

        # Validate from
        if _from:
            length = len(_from) # implement this logic with lambda function
            if length <= 5 or length >= 17:
                return jsonify({"message": "", "error": err_msg % _from})

            # Validate to
            if to:
                length = len(to)
                if length <= 5 or length >= 17:
                    return jsonify({"message": "", "error": err_msg % to})

                # Validate text
                if text:
                    length = len(text)
                    if length <= 0 or length >= 121:
                       return jsonify({"message": "", "error": err_msg % text})
                else:
                    return jsonify({"message": "", "error": "text is missing"})
            else:
                return jsonify({"message": "", "error": "to is missing"})
        else:
            return jsonify({"message": "", "error": "from is missing"})

        return constants.VALIDATED


    def verifyParams(_from,  to, text, msgtype=""):
        """Veryfies given params with db values . """

        err_msg = "%s parameter not found"

        # initialize db params
        rs = app.config['rs']
        ps = app.config['ps']

        retVal = validateParamas(_from, to, text)

        if retVal == constants.VALIDATED:
            
            # DB operation to check if from is not present
            if msgtype == constants.OUTBOUND:
                sql = """SELECT number FROM phone_number where \
                         number='%s';""" %_from
                rows = ps.fireQuery(sql)
                if not rows:
                    return jsonify({"message": "", "error": err_msg % "from"})

            # DB operation to check if to is not present
            if msgtype == constants.INBOUND:
                sql = """SELECT number FROM phone_number where number='%s';""" %to
                rows = ps.fireQuery(sql)
                if not rows:
                    return jsonify({"message": "", "error": err_msg % "to"})

            if "STOP" in text:
                key = _from+to

                # if inbound message, store it in redis
                if msgtype == constants.INBOUND:
                    lcounter = rs.redis_conn.scard("lcounter")

                    if not lcounter:
                        # set limit_counter to expire after 4 hours.
                        rs.redis_conn.set(str(key), text, ex=14400)
                        # set limit_counter to expire after 24 hours.
                        rs.redis_conn.set("limit_counter", 1, ex=86400)
                        rs.redis_conn.sadd("lcounter", 1)
                    elif int(lcounter) <= 50:
                        rs.redis_conn.set(str(key), text, ex=14400)
                        lock.acquire()
                        rs.redis_conn.sadd("lcounter", int(lcounter)+1)
                        lock.release()
                    else:
                        err_msg = "limit reached for from %s" % _from
                        return jsonify({"message": "", "error": err_msg})

                # if outbound message, verify from & to and report error message
                if msgtype == constants.OUTBOUND:
                    if rs.redis_conn.get(_from+to) or rs.redis_conn.get(to+_from):
                        err_msg = "sms from %s to %s blocked by STOP request" % (_from, to)
                        return jsonify({"message": "", "error": err_msg})
            if msgtype == constants.OUTBOUND and (
                rs.redis_conn.get(_from+to) or rs.redis_conn.get(to+_from)):
                err_msg = "sms from %s to %s blocked by STOP request" % (_from, to)
                return jsonify({"message": "", "error": err_msg})
        else:
            return retVal

        # When everything is fine.
        if msgtype == constants.INBOUND:
            return jsonify({"message": "inbound sms ok", "error": ""})
        else:
            return jsonify({"message": "outbound sms ok", "error": ""})

    def authenticate(auth, data, msgtype):
        """Authenticate with the provided username & password. """

        # payload related
        data = json.loads(data)
        _from = data["from"]
        to = data["to"]
        text = data["text"]

        # auth creds
        # Note: as the flask test_client doesn't support auth option in post
        # request to validate authentication.
        # verify, if it testcase or normal usecase
        if "test" in data:
            auth = data["test"]

        username = auth["username"]
        password = auth["password"]
        ps = app.config['ps']

        try:
            sql = """SELECT username auth_id FROM account where username\
                     ='%s' AND auth_id='%s';""" %(username, password)
            rows = ps.fireQuery(sql)
            if not rows:
                resp =jsonify({"message": "", "error": "authentication failed"})
                resp.status_code = 403
                return resp

            return verifyParams(_from, to, text, msgtype=msgtype)

        except:        
            return jsonify({"message": "", "error": "unknown failure"})

    def authCreds(creds):

        return creds

    @app.route('/outbound/sms/',  methods=['POST'])
    def ouboundSMS():
        """outbound request """

        if  request.method != 'POST':
            resp =jsonify({"message": "", "error":
                    "%s not supported" % request.method})
            resp.status_code = 505
            return resp
        # auth = request.authorization
        auth = request.authorization
        # auth = {"username": "azr1", "password": "20S0KPNOIM"}

        return authenticate(auth, request.data, constants.OUTBOUND)


    @app.route('/inbound/sms/',  methods=['POST'])
    def inboundSMS():
        """inbound request """

        if  request.method != 'POST':
            resp =jsonify({"message": "", "error":
                    "%s not supported" % request.method})
            resp.status_code = 505
            return resp
            # return "HTTP 505"
        # auth = authCreds(request.authorization)
        auth = request.authorization

        # return authenticate(auth, request.data, constants.INBOUND)
        return authenticate(auth, request.data, constants.INBOUND)

    return app


# if __name__ == '__main__':
def main():
    sobjs = verify_services()
    if sobjs:
        ps = sobjs[0]
        rs = sobjs[1]
        thread = threading.Thread(name='clean', target=timeout, args=())
        thread.daemon = True
        thread.start()
        app = messageApplication()
        app.run(debug=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
                # Clean the resource if exists, to avoid stale entries
                rs.redis_conn.set("limit_counter", 0)
                while rs.redis_conn.scard("lcounter") > 0:
                    rs.redis_conn.spop("lcounter")
    else:
        print "Postgressql or Redis servers are not running.Start the servers."

main()
