import ast
import json
import os

from flask import url_for
from flask import request


numbers = ["441224980093", "441887480051", "441873440028", "441873440017", "441970450009", "441235330075", "441235330053", "441235330044", "441235330078", "34881254103", "61871112946", "61871112915", "61881666904 4924195509196", "4924195509197", "4924195509195", "4924195509012", "4924195509193", "4924195509029", "4924195509192", "4924195509194", "31297728125", "3253280312", "3253280311", "3253280315", "3253280313", "3253280329", "441224459508", "441224980086", "441224980087", "441224980096", "441224980098", "441224980099", "441224980100", "441224980094", "441224459426", "13605917249", "61881666939", "61871112913", "61871112901", "61871112938", "61871112934", "61871112902", "61881666926", "61871705936", "61871112920", "61881666923", "61871112947", "61871112948", "61871112921", "61881666914", "61881666942"]


class TestApp():


    # param missing testcases
    def test_outbound_to_missing(self, client):
        data = {"from": "4924195509049", "to": "", "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'to is missing'}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg
        assert resp.status_code == 200

    def test_outbound_from_missing(self, client):
        data = {"from": "", "to": "4924195509192", "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'from is missing'}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg

    def test_outbound_text_missing(self, client):
        data = {"from": "4924195509049", "to": "4924195509192", "text": "",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'text is missing'}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg

    def test_inbound_to_missing(self, client):
        data = {"from": "4924195509049", "to": "", "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'to is missing'}
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg

    def test_inbound_from_missing(self, client):
        data = {"from": "", "to": "4924195509192", "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'from is missing'}
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg

    def test_inbound_text_missing(self, client):
        data = {"from": "4924195509049", "to": "4924195509192", "text": "",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'text is missing'}
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg


    def test_inbound_OK(self, client, production=True):
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {"error": "", "message": "inbound sms ok"}
        # with mock.patch.object(PostgresSQLServer,
        #                        "fireQuery",
        #                         return_value=('fake', 'data')) as ps_mocked:
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg
        os.system("redis-cli FLUSHDB")

    def test_outbound_OK(self, client, production=True):
        os.system("redis-cli FLUSHDB")
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hey Auzmor",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {"error": "", "message": "outbound sms ok"}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg
        os.system("redis-cli FLUSHDB")

    def test_outbound_STOP(self, client,  production=True):
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error':
            'sms from 4924195509049 to 4924195509192 blocked by STOP request'}
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg
        os.system("redis-cli FLUSHDB")


    def test_outbound_200(self, client):
        data = {"from": "4924195509049", "to": "", "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'to is missing'}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert resp.status_code == 200
        os.system("redis-cli FLUSHDB")

    def test_inbound_200(self, client, production=True):
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {"error": "", "message": "inbound sms ok"}
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        assert resp.status_code == 200
        os.system("redis-cli FLUSHDB")

    def test_inbound_405(self, client, production=True):
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {"error": "", "message": "inbound sms ok"}
        resp = client.get('/inbound/sms/', data=json.dumps(data))
        assert resp.status_code == 405
        os.system("redis-cli FLUSHDB")

    def test_outbound_405(self, client, production=True):
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hello",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {"error": "", "message": "inbound sms ok"}
        resp = client.get('/outbound/sms/', data=json.dumps(data))
        assert resp.status_code == 405
        os.system("redis-cli FLUSHDB")

    def test_inbound_403(self, client, production=True):
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hey there!, STOP",
                "test": {"username": "azr", "password": "20S0KPNOIM"}}
        resp_msg = {"error": "", "message": "inbound sms ok"}
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        assert resp.status_code == 403
        os.system("redis-cli FLUSHDB")

    def test_outbound_403(self, client, production=True):
        data = {"from": "4924195509049", "to": "4924195509192",
                "text": " Hello",
                "test": {"username": "azr", "password": "20S0KPNOIM"}}
        resp_msg = {"error": "", "message": "inbound sms ok"}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert resp.status_code == 403
        os.system("redis-cli FLUSHDB")

    def test_invalid_to(self, client):
        data = {"from": "4924195509049", "to": "12", "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': '12 is invalid'}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg

    def test_invalid_from(self, client):
        data = {"from": "5464", "to": "4924195509192", "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': '5464 is invalid'}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg

    def test_to_param_not_found(self, client, production=True):
        data = {"from": "4924195509049", "to": "492509192",
                "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'to parameter not found'}
        resp = client.post('/inbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg
        os.system("redis-cli FLUSHDB")

    def test_from_param_not_found(self, client, production=True):
        data = {"from": "492419549", "to": "4924195509192",
                "text": " Hey there!, STOP",
                "test": {"username": "azr1", "password": "20S0KPNOIM"}}
        resp_msg = {'message': '', 'error': 'from parameter not found'}
        resp = client.post('/outbound/sms/', data=json.dumps(data))
        assert ast.literal_eval(resp.data) == resp_msg
        os.system("redis-cli FLUSHDB")

    def test_limit_reached_for_from(self, client, production=True):
        count = 0
        for number in numbers:
            data = {"from": "4924195509049", "to": number,
                    "text": " Hey there!, STOP",
                    "test": {"username": "azr1", "password": "20S0KPNOIM"}}
            resp = client.post('/inbound/sms/', data=json.dumps(data))
            count += 1

        resp_msg = {"error": "limit reached for from 4924195509049",
                    "message": ""}
        assert ast.literal_eval(resp.data) == resp_msg
        os.system("redis-cli FLUSHDB")

