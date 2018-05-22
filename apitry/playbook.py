import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        #print json.dumps({host.name: result._result}, indent=4)
        print json.dumps(result._result)

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        print "unreachable"


    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        print "failed"

    def v2_runner_on_no_hosts(self, task):
        self.runner_on_no_hosts()
        print "no_hosts"


Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become',
                                 'become_method', 'become_user', 'check', 'diff'])
# initialize needed objects
loader = DataLoader()
options = Options(connection='smart', module_path='', forks=100, become=None, become_method=None, become_user=None, check=False,
                  diff=False)
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()

# create inventory and pass to var manager
inventory = InventoryManager(loader=loader, sources='10.100.62.75,169.254.1.48,10.101.30.179')


# inventory.add_group(group=[])
# print('inventory',inventory.get_groups_dict())
variable_manager = VariableManager(loader=loader, inventory=inventory)
print('inventory', variable_manager.get_vars())
# variable_manager.extra_vars('')

# create play with tasks
play_source = {
    u'gather_facts': u'no',
    u'tasks': [
        # {u'set_fact': {'ansible_ssh_common_args':'-o ProxyCommand="ssh -p52000 -W %h:%p root@114.55.126.93"'}},
        {u'shell': u'ls -lh', u'name': u'li'},
        {u'shell': u'touch ~/{{app_name}}', u'name': u'zi'}],
    u'hosts': u'localhost'
}

variable_manager.extra_vars = {'app_name': 'test'}
play1 = Play().load(play_source, variable_manager=variable_manager, loader=loader)
play2 = Play().load(play_source, variable_manager=variable_manager, loader=loader)

tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
          )
    result = tqm.run(play1)
finally:
    if tqm is not None:
        tqm.cleanup()
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)