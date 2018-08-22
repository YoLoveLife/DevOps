PING_PLAY_SOURCE = [{
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
                        'ping': ''
                }
        ]
},]


DISK_PLAY_SOURCE = [{
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
                        'shell': 'df -hP|grep \/$ |awk \'{print $5}\''
                }
        ]
},]


UPTIME_PLAY_SOURCE = [{
        'hosts': None,
        'remote_user': 'root',
        'gather_facts': 'yes',
        'tasks': [
                {
                        'set_fact': {
                                'ansible_ssh_common_args':
                                        '-o ProxyCommand="ssh -p{{JUMPER_PORT}} -i {{KEY}} -W %h:%p root@{{JUMPER_IP}}"'
                        }
                },{
                        'shell': 'echo cpus{{ ansible_processor_vcpus }}'
                },{
                        'shell': 'uptime'
                }
        ]
}]