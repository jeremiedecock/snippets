# Source:
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# https://gist.github.com/miguelgrinberg/5614326

from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


# Since this is a web service client applications will expect that we always respond with JSON

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# THE INITIAL DATABASE ########################################################

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# GET THE LIST OF RECORDED TASKS ##############################################

# To test this function we can use the following curl command:
# $ curl -i http://localhost:5000/hello/api/v1.0/tasks

@app.route('/hello/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# GET THE REQUESTED TASK ######################################################

# Here we get the id of the task in the URL, and Flask translates it into the task_id argument that we receive in the function.
# With this argument we search our tasks array. If the id that we were given does not exist in our database then we return the familiar error code 404, which according to the HTTP specification means "Resource Not Found", which is exactly our case.
# If we find the task then we just package it as JSON with jsonify and send it as a response, just like we did before for the entire collection.

# To test this function we can use the following curl command:
# $ curl -i http://localhost:5000/hello/api/v1.0/tasks/2
# $ curl -i http://localhost:5000/hello/api/v1.0/tasks/3

@app.route('/hello/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# ADD A TASK ##################################################################

# The request.json will have the request data, but only if it came marked as JSON. If the data isn't there, or if it is there, but we are missing a title item then we return an error code 400, which is the code for the bad request.
# We then create a new task dictionary, using the id of the last task plus one (a cheap way to guarantee unique ids in our simple database). We tolerate a missing description field, and we assume the done field will always start set to False.
# We append the new task to our tasks array, and then respond to the client with the added task and send back a status code 201, which HTTP defines as the code for "Created".

# To test this function we can use the following curl command:
# $ curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/hello/api/v1.0/tasks
# $ curl -i http://localhost:5000/hello/api/v1.0/tasks

@app.route('/hello/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# MODIFY A TASK ###############################################################

# For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database.

# To test this function we can use the following curl command:
# $ curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/hello/api/v1.0/tasks/2

@app.route('/hello/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# DELETE A TASK ###############################################################

@app.route('/hello/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

###############################################################################

if __name__ == '__main__':
    app.run(debug=True)
