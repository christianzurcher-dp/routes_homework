from flask import jsonify, request
import json
from uuid import uuid4


def users_table_read():
    try:
        with open('users_table.json', 'r') as openfile:

            return json.load(openfile)

    except:

        return []


def users_table_write(records):
    with open('users_table.json', 'w') as outfile:
        json.dump(records, outfile)


def user_add():
    post_data = request.form if request.form else request.json

    user = {
        'user_id': str(uuid4()),
        'first_name': post_data['first_name'],
        'last_name': post_data['last_name'],
        'email': post_data['email'],
        'phone_number': post_data['phone_number'],
        'active': True
    }

    user_records = users_table_read()
    user_records.append(user)

    return jsonify(f"{user['first_name']} has been added"), 201


def users_get_all():
    users_list = users_table_read()

    if len(users_list) == 0:
        return jsonify("No users found"), 404

    return jsonify(users_list), 200


def user_get_by_id(user_id):
    user_data = users_table_read()

    if len(user_data) == 0:
        return jsonify("No user found"), 404

    for user in user_data:
        if user['user_id'] == user_id:

            return jsonify(user), 200

    return jsonify(f"user with ID: {user_id} not found"), 404


def user_update_by_id(user_id):
    user_data = users_table_read()
    post_data = request.form if request.form else request.json

    if len(user_data) == 0:
        return jsonify("No user found"), 404

    for user in user_data:
        if user['user_id'] == user_id:

            for key in user.keys():
                try:
                    user[key] = post_data[key]
                except:
                    pass

            users_table_write(user_data)

            return jsonify(f"user: {user['name']} has been updated")

    return jsonify(f"user with ID: {user_id} not found"), 404


def user_delete_by_id(user_id):
    user_data = users_table_read()

    if len(user_data) == 0:

        return jsonify("No user found"), 404

    for index, user in enumerate(user_data):
        if user['user_id'] == user_id:
            user_data.pop(index)

            users_table_read(user_data)

            return jsonify(f"user: {user['name']} has been removed")


def user_activity(user_id):
    user_data = users_table_read()

    if len(user_data) == 0:

        return jsonify("No user found"), 404

    for user in user_data:
        if user['user_id'] == user_id:

            user['active'] = not user['active']

            users_table_write(user_data)

            return jsonify(user), 200

    return jsonify(f"user with ID: {user_id} not found"), 404
