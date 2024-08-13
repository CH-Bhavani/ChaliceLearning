from chalice import Chalice, Rate, Response
import uuid

app = Chalice(app_name="helloworld")

users = [
    {"id": "1", "first_name": "John", "last_name": "Doe"},
    {"id": "2", "first_name": "Jane", "last_name": "Smith"}
]

# GET endpoint
@app.route("/", methods=['GET'])
def index():
    return {"hello": "world"}

# GET endpoint with path parameter
@app.route("/greet/{name}", methods=['GET'])
def greeting(name):
    for user in users:
        if user['first_name'].lower() == name.lower():
            return {"message": f"Hi! {user['first_name']} {user['last_name']}"}
    return Response(body={"message": "User not found"},
                    status_code=404,
                    headers={'Content-Type': 'application/json'})

# POST endpoint to create a user
@app.route("/users", methods=['POST'])
def create_user():
    request = app.current_request
    user = request.json_body
    users.append(user)
    return Response(body={"message": "User created", "user": user},
                    status_code=201,
                    headers={'Content-Type': 'application/json'})

# GET endpoint to list all users
@app.route("/users", methods=['GET'])
def list_users():
    return {"users": users}

# PUT endpoint to update a user
@app.route("/users/{user_id}", methods=['PUT'])
def update_user(user_id):
    request = app.current_request
    updated_user = request.json_body
    for user in users:
        if user['id'] == user_id:
            user.update(updated_user)
            return {"message": f"User {user_id} updated", "user": user}
    return Response(body={"message": f"User {user_id} not found"},
                    status_code=404,
                    headers={'Content-Type': 'application/json'})

# DELETE endpoint to delete a user
@app.route("/users/{user_id}", methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return {"message": f"User {user_id} deleted"}

# Scheduled task
@app.schedule(Rate(1, unit=Rate.MINUTES))
def periodic_task(event):
    print("I'm running every 1 minute")
    return {"hello": "world every 1 minute"}