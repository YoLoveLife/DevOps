class Task(object):
    def __init__(self,module="shell",args="",register='shell_out'):
        self.module=module
        self.args=args
        self.register=register

    def pop_task(self):
        return dict(action=dict(module=self.module,args=self.args),register=self.register)

    def __str__(self):
        return "[module_name:%s][args:%s][register:%s]"%(self.module,self.args,self.register)

class Tasks(object):
    def __init__(self):
        self.task_list=[]

    def __str__(self):
        return self.task_list

    def push_task(self,task):
        self.task_list.append(task)

    def pop_tasks(self):
        list=[]
        for task in self.task_list:
            list.append(task.pop_task())
        return list

if __name__ == '__main__':
    a=Task(module="shell",args="ls /etc")
    b=Task(module="shell",args="ls /usr")
    c=Task(module="shell",args="ls /")

    s=Tasks()
    s.push_task(a)
    s.push_task(b)
    s.push_task(c)
    print(s.pop_tasks())
    print(s.__str__())