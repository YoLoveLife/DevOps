from yosible.tasks.tasks import Tasks,Task
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars import VariableManager
from apps.execute.callback import ResultCallback
from playbook import Playbook
from yosible.vars.args import option, HOST_LIST

class Ansible():
    def __init__(self,host_file):
        self.options = option
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = dict(vault_pass='')
        self.results_callback = ResultCallback()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=host_file)
        self.variable_manager.set_inventory(self.inventory)

    def add_extendvars(self,newext):
        self.variable_manager.extra_vars=newext

    def set_playbook(self,pb):
        self.playbook=pb
        self.add_extendvars(self.playbook.ext_vars)

    def set_callback(self,callback):
        self.results_callback = callback

    def run_playbook(self):
        tqm=pop_TaskqueueManager(self)
        try:
            result =tqm.run(Play().load(self.playbook.pop_playbook()))
            return result
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

    b=Task(module="script",args="~/ddr.sh")

    s=Tasks()
    s.push_task(b)
    A=Ansible()
    pb.push_tasks(s)
    A.set_playbook(pb)

    A.run_playbook()
