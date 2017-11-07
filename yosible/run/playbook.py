from yosible.tasks.tasks import Task,Tasks
class Playbook():
    def __init__(self,pbname,pbfacts):
        self.name=pbname
        self.hosts='all'
        self.gather_facts=pbfacts
        self.ext_vars={}
        self.tasks=Tasks()

    def push_vars(self,new_vars):#Rewrite
        self.ext_vars=new_vars

    def push_task(self,task):
        self.tasks.push_task(task=task)

    def push_tasks(self,tasks):#Rewrite
        self.tasks=tasks

    def pop_tasks(self):
        return self.tasks.pop_tasks()

    def pop_playbook(self):
        print(dict(name=self.name,hosts=self.hosts,gather_facts=self.gather_facts,tasks=self.tasks.pop_tasks()))
        return dict(name=self.name,hosts=self.hosts,gather_facts=self.gather_facts,tasks=self.tasks.pop_tasks())

if __name__ == "__main__":
    p=Playbook('ddr','no')

    a=Task(module="shell",args="ls /etc")
    b=Task(module="shell",args="ls /usr")
    c=Task(module="shell",args="ls /")

    s=Tasks()
    s.push_task(a)
    s.push_task(b)
    s.push_task(c)

    p.push_tasks(s)
    print(p.pop_playbook())