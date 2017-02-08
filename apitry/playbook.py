import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import json
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
        print "aaa"

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        print "bbb"

    def v2_runner_on_no_hosts(self, task):
        self.runner_on_no_hosts()
        print "ccc"


Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
# initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()
options = Options(connection='smart', module_path='', forks=100, become=None, become_method=None, become_user=None, check=False)
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()

# create inventory and pass to var manager
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list="/etc/ansible/hosts")
variable_manager.set_inventory(inventory)
# create play with tasks
play_source =  dict(
        name = "Ansible Play",
        hosts = 'redis-server',
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='ping', args=''), register='shell_out'),
            #dict(action=dict(module='shell', args='hostname'), register='shell_out'),
            #dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
         ]
    )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

# actually run it
tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords={},
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
          )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()