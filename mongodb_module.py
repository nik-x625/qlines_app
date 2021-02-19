from pymongo import MongoClient
import logging
import datetime


logger = logging.getLogger(__name__)

client = MongoClient('127.0.0.1', 22022)
db = client['platform']
#sensor_collection = db['sensor_data']
#contact_submission = db['contact_submission']


def update_profile_in_db(key, doc):
    client = MongoClient('127.0.0.1', 22022)
    db = client.platform
    coll = db.pages
    #contact_submission = db['contact_submission']

    doc['ts'] = datetime.datetime.now()
    coll.update(key, doc, upsert=True)


def read_user_doc(username):
    users = db['users']
    user_doc = users.find_one({'username': username})
    return user_doc


def write_to_user_doc(key, item):
    users = db['users']
    users.update_one(
        key,
        {
            "$set": item,
            "$currentDate": {"lastModified": True}
        }
    )


def update_sensor_data(doc):
    sensor_collection.insert_one(doc)


def contact_submission_update(doc):
    #logit('going to write in db')
    contact_submission.insert_one(doc)
    #logit('db writing is done')
    return True


def create_new_user(doc):
    users = db['users']
    users.insert_one(doc)


def read_users_collection():
    return db['users'].find()


if __name__ == '__main__':

    '''
    read_user_doc('test_user_name')

    to_store = {'car': 'ford'}
    write_to_user_doc({'username': 'test_user_name'}, to_store)

    print
    "After updating the user document: "
    print
    read_user_doc('test_user_name')
    user = read_user_doc('test_user_name')
    print
    #'user car is: ', user['car']
    new_user = {'username': 'New boy', 'car': 'Nissa'}
    create_new_user(new_user)


    print
    "After adding new user:"
    print
    read_user_doc('New boy')

    # sample to print the whole collection docs
    for i in read_users_collection():
        print
        "Items from users collection: ", i
    '''
    update_sensor_data({'aa': 10, 'bb': 20})
