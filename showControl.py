import json

with open("config.json") as configFile:
    config = json.load(configFile)


def toJson_and_delExtras(rawPosts, count, COUNT_POSTS=config['settings']['COUNT_POSTS']):
    posts = []

    for i in rawPosts:
        posts.append(i.toJson())

    for i in range(0, COUNT_POSTS * (count - 1)):
        if posts:
            posts.pop(0)

    return posts


def toJsonRole(role):
    jsonData = {'role': role}
    return jsonData
