from app import app
import unittest




class ApiTest(unittest.TestCase):

    user1 = {
        "id": 1,
        "first_name": "Ehsan",
        "last_name": "Rahi",
        "age": 26
       }  

    new_user = {
            "id": 2,
            "first_name": "Ali",
            "last_name": "Hassani",
            "age": 35
            } 

    def test_main_page(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_get_user(self):
        tester = app.test_client(self)
        response = tester.get("/users/1")
        self.assertEqual(self.user1, response.json)


    def test_insert_new_user(self):
        tester = app.test_client(self)
        response = tester.post("/users/", json=self.new_user)
        server_users = tester.get("/users", follow_redirects=True)
        self.assertEqual(self.new_user, response.json)
        self.assertIn(self.new_user, server_users.json)
    
    def test_delete(self):
        tester = app.test_client(self)
        tester.delete("/users/2")
        server_users = tester.get("/users", follow_redirects=True)
        self.assertNotIn(self.new_user, server_users.json)

    def test_update_user(self):
        tester = app.test_client(self)
        updated_user = {"age":23}
        response = tester.put("/users/1", json=updated_user)
        server_users = tester.get("/users/1")
        self.assertEqual(response.json, server_users.json)
        tester.put("/users/1", json=self.user1)
    

    def test_get_all_users(self):
        tester = app.test_client(self)
        response = tester.get("/users", follow_redirects=True)
        length = len(response.json)
        self.assertEqual(1, length)
        self.assertIn(self.user1, response.json)
  
        


 


if __name__ == "__main__":
    unittest.main()
