# import os
# import json

# def get_items():
#     return json.dumps(os.listdir("."), indent=4)

# def create_item(key, payload, createnew=True):
#     message = "updated: {}".format(key)
#     if createnew: message = "created: {}".format(key)

#     return json.dumps({"message": message,
#                        "payload": json.load(payload)},
#                       indent=4)