PLAY_SOURCE = [
        {
                'hosts': None,
                'remote_user': 'root',
                'gather_facts': 'no',
                'tasks': [
                        {
                                'script': '{{TOOL}}/yotelnet 127.0.0.1 {{ REDIS_PORT }}',
                                'register': 'ALREADY_INSTALL'
                        }
                ],
                # 'roles': [
                #         {
                #                 'role': '{{ROLE}}',
                #                 'when': 'ALREADY_INSTALL!=False',
                #         }
                # ]
        },
]
