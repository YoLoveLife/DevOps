from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars import VariableManager
from callback import ResultCallback
from playbook import Playbook
from yosible.tasks.tasks import Task,Tasks
from yosible.vars.args import option, HOST_LIST


class Ansible():
    def __init__(self):
        self.options = option
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = dict(vault_pass='')
        self.results_callback = ResultCallback()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=HOST_LIST)
        self.variable_manager.set_inventory(self.inventory)

    def add_extendvars(self,newext):
        self.variable_manager.extra_vars=newext

    def set_playbook(self,pb):
        self.playbook=pb
        self.add_extendvars(self.playbook.ext_vars)

    def run_playbook(self):
        tqm=pop_TaskqueueManager(self)
        try:
            result =tqm.run(Play().load(self.playbook.pop_playbook()))
        finally:
            if tqm is not None:
                tqm.cleanup()

def pop_TaskqueueManager(ansible):
    tqm = TaskQueueManager(inventory=ansible.inventory,
                                variable_manager=ansible.variable_manager,
                                loader=ansible.loader,
                                options=ansible.options,
                                passwords=ansible.passwords,
                                stdout_callback=ansible.results_callback,)
    return tqm


if __name__ == "__main__":
    pb=Playbook('ddr','no')
    pb.push_vars({'prefix':'/usr/local','base_dir':'/usr/local/tomcat'})

    b=Task(module="shell",args="ls /")

    s=Tasks()
    s.push_task(b)

    A=Ansible()
    pb.push_tasks(s)
    A.set_playbook(pb)
    A.run_playbook()
