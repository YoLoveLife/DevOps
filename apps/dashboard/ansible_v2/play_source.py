PLAY_SOURCE = [{
        'hosts': None,
        'remote_user': 'root',
        'gather_facts': 'no',
        'tasks': [
                {
                        'set_fact':{
                                'ansible_ssh_common_args':
                                        '-o ProxyCommand="ssh -p{{JUMPER_PORT}} -i {{KEY}} -W %h:%p root@{{JUMPER_IP}}"'
                        }
                },
                {
                        'shell': 'df -h|grep \/$ |awk \'{print $5}\''
                }
        ]
},]
