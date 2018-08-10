PLAY_SOURCE = {
        'hosts': None, # need to reload
        'remote_user': 'root',
        'gather_facts': 'no',
        'tasks':[
                {
                        'set_fact': {
                                'ansible_ssh_common_args': '-oProxyCommand="ssh -p52000 -i {{KEY}} -W %h:%p root@{{JUMPER}}"'
                        }
                },
                {
				'name': '测试',
				'shell': 'touch /deveops'
			    }
        ]
        # 'roles': [
        #     'ddr'
        # ]
}
