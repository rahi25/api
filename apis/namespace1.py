from flask_restplus import fields, Resource, Namespace

api = Namespace("users", description="Users Operations")

user = api.model("User",{
                        "id": fields.Integer(required=True, description="The User Id"),
                        "first_name": fields.String(required=True, description="First Name"),
                        "last_name": fields.String(required=True, description="Last Name"),
                        "age": fields.Integer(required=True, description="Age")    
                        })




class MakeUser:
    def __init__(self):
        self.counter = 0
        self.users = []
   
    def get(self, id):
        for user in self.users:
            if user["id"] == id:
                return user
        api.abort(404, f"User with ID = {id} dose not exist")

    def create(self, data):
        user = data
        user["id"] = self.counter = self.counter + 1
        self.users.append(user)
        return user
    
    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user
    
    def delete(self, id):
        user = self.get(id)
        self.users.remove(user)


mu = MakeUser()
mu.create({
             "id": 1,
             "first_name": "Ehsan",
             "last_name": "Rahi", 
             "age": 26    
            })

@api.route("/")
class UsersList(Resource):

    @api.marshal_with(user)
    def get(self):
        """ Take List of Users """
        return mu.users

    @api.expect(user)
    def post(self):
        """ Create New User """
        return mu.create(api.payload), 201

@api.route("/<int:id>")
@api.response(404, "User Not Found")
class User(Resource):

    @api.marshal_with(user)
    def get(self,id):
        """ Given User """
        return mu.get(id)

    @api.expect(user)
    @api.marshal_with(user)
    def put(self, id):
        """ Edit User """
        return mu.update(id, api.payload)

    @api.response(204, "Deleted User")
    def delete(self, id):
        """ Delete User """
        mu.delete(id)
        return "Delete This user {id} Successfully", 204
