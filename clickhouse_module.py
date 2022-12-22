import clickhouse_connect


client_handler = clickhouse_connect.get_client(
    host='localhost', port='7010', username='default')


def fetch_data_per_param(user_name, client_name, param_name, limit, table_name='table1'):
    res = client_handler.query("SELECT param_name, ts, param_value FROM {} WHERE user_name='{}' and client_name='{}' and param_name='{}' ORDER BY ts DESC LIMIT {}".format(
        table_name, user_name, client_name, param_name, limit))
    return res


def fetch_device_overview(user_name, table_name, limit):
    # res = client_handler.query("SELECT distinct(client_name) FROM {} table_name WHERE user_name='{}' ORDER BY ts DESC LIMIT {}".format(
    #    table_name, user_name, limit))

    res = {
        'data': [
            {'id': 1, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
            {'id': 2, 'user_name': 'user1', 'client_name': 'cpe1', 'last_message': 23423,
             'first_message': 123, 'description': 'some desc here', 'offline_for': 3242},
        ],

        'recordsFiltered': 10,
        'recordsTotal': 230,
    }

    # res = {'data': [
    #     {'id': 1, 'name': 'xyNicholas Brown', 'age': 36, 'address': '8054 Bridges River Apt. 689, Blackwellland, MI 46398', 'phone': '236.648.5446', 'email': 'scottdowns@example.net'
    #      },
    #     {'id': 2, 'name': 'Michael Flynn', 'age': 61, 'address': '530 Cathy Summit, Juliechester, RI 08632', 'phone': '895-231-5105x67156', 'email': 'pbrown@example.net'
    #      },
    #     {'id': 3, 'name': 'Thomas Welch', 'age': 21, 'address': '12451 Vaughn Groves Apt. 608, East Robin, NJ 54656', 'phone': '(742)357-2317x417', 'email': 'crystal83@example.com'
    #      },
    #     {'id': 4, 'name': 'Justin Hernandez', 'age': 71, 'address': '853 Adams Row Apt. 029, Morristown, NC 58068', 'phone': '428-042-4603', 'email': 'johnsonkimberly@example.net'
    #      },
    #     {'id': 5, 'name': 'Margaret Harrison', 'age': 78, 'address': '649 Michael Island Suite 931, Lisamouth, MS 51279', 'phone': '001-043-736-7329x0178', 'email': 'zsanchez@example.com'
    #      },
    #     {'id': 6, 'name': 'Kevin Johnson', 'age': 72, 'address': '5103 Vaughn Stravenue, Thomasmouth, CA 37817', 'phone': '001-113-509-6047', 'email': 'nedwards@example.com'
    #      },
    #     {'id': 7, 'name': 'Monique Williams', 'age': 54, 'address': '480 Mario Trail, Beckshire, WA 68889', 'phone': '(612)059-2253', 'email': 'katherinebass@example.net'
    #      },
    #     {'id': 8, 'name': 'Lindsay Lopez', 'age': 77, 'address': '2632 Gomez Camp, East Sethfurt, IN 59235', 'phone': '391.310.8184x60195', 'email': 'william28@example.org'
    #      },
    #     {'id': 9, 'name': 'Andrea Martinez', 'age': 45, 'address': '21133 Ward Port Suite 591, Lake Andrew, AL 56716', 'phone': '+1-409-197-6807x5376', 'email': 'georgechen@example.com'
    #      },
    #     {'id': 10, 'name': 'Brenda Haas', 'age': 34, 'address': '87134 Burnett Rapid, Port Richardside, FL 25913', 'phone': '278-167-0407x34146', 'email': 'zachary91@example.com'
    #      }
    # ], 'total': 102
    # }

    return res
