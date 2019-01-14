from flask_restplus import Api

from apis.namespace1 import api as ns1

api = Api (title="User API", version="1.0", description=" Manage Users By API")

api.add_namespace(ns1)