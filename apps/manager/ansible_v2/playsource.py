# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
PING_PLAY_SOURCE = [
        {
                'hosts': None,
                'remote_user': 'root',
                'gather_facts': 'no',
                'tasks': [
                        {
                                'set_fact': {
                                        'ansible_ssh_common_args':
                                                '-o ProxyCommand="ssh -p{{JUMPER_PORT}} -i {{KEY}} -W %h:%p root@{{JUMPER_IP}}"'
                                }
                        },
                        {
                                'ping': ''
                        }
                ]
        },
]


DISK_SPACE_PLAY_SOURCE = [
        {
                'hosts': None,
                'remote_user': 'root',
                'gather_facts': 'no',
                'tasks': [
                        {
                                'set_fact': {
                                        'ansible_ssh_common_args':
                                                '-o ProxyCommand="ssh -p{{JUMPER_PORT}} -i {{KEY}} -W %h:%p root@{{JUMPER_IP}}"'
                                }
                        },
                        {
                                'shell': 'df -hP|grep \/$ |awk \'{print $5}\''
                        }
                ]
        },
]

DISK_INODE_PLAY_SOURCE = [
        {
                'hosts': None,
                'remote_user': 'root',
                'gather_facts': 'no',
                'tasks': [
                        {
                                'set_fact': {
                                        'ansible_ssh_common_args':
                                                '-o ProxyCommand="ssh -p{{JUMPER_PORT}} -i {{KEY}} -W %h:%p root@{{JUMPER_IP}}"'
                                }
                        },
                        {
                                'shell': 'df -hiP|grep \/$ |awk \'{print $5}\''
                        }
                ]
        },
]


UPTIME_PLAY_SOURCE = [
        {
                'hosts': None,
                'remote_user': 'root',
                'gather_facts': 'yes',
                'tasks': [
                        {
                                'set_fact': {
                                        'ansible_ssh_common_args':
                                                '-o ProxyCommand="ssh -p{{JUMPER_PORT}} -i {{KEY}} -W %h:%p root@{{JUMPER_IP}}"'
                                }
                        },
                        {
                                'shell': 'echo cpus{{ ansible_processor_vcpus }}'
                        },
                        {
                                'shell': 'uptime'
                        }
                ]
        },
]
