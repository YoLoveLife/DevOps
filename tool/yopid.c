#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#define BUF_SIZE 1024

void getPidByName(pid_t *pid, char *task_name)
{
    DIR *dir;
    struct dirent *ptr;
    FILE *fp;
    char filepath[50];
    char cur_task_name[50];
    char buf[BUF_SIZE];

    dir = opendir("/proc");
    if (NULL != dir)
    {
        while ((ptr = readdir(dir)) != NULL) //循环读取/proc下的每一个文件/文件夹
        {
            //如果读取到的是"."或者".."则跳过，读取到的不是文件夹名字也跳过
            if ((strcmp(ptr->d_name, ".") == 0) || (strcmp(ptr->d_name, "..") == 0))
            continue;
            if (DT_DIR != ptr->d_type)
            continue;

            sprintf(filepath, "/proc/%s/cmdline", ptr->d_name);//生成要读取的文件的路径
            fp = fopen(filepath, "r");
            if (NULL != fp)
            {
                if( fgets(buf, BUF_SIZE-1, fp)== NULL ){
                    fclose(fp);
                    continue;
                }
                sscanf(buf, "%s", cur_task_name);
                //如果文件内容满足要求则打印路径的名字（即进程的PID）
                printf("P%s\n", ptr->d_name);
                printf("A%s\n",task_name);
                printf("B%s\n",buf);
                if (!strstr(task_name, cur_task_name)){
                    sscanf(ptr->d_name, "%d", pid);
                }
                fclose(fp);
            }
        }
        closedir(dir);
    }
}


void main(int argc, char** argv)
{
    char task_name[50];
    pid_t pid = getpid();

    //printf("pid of this process:%d\n", pid);
    //getNameByPid(pid, task_name);
    //printf("getNameByPid:%s\n", task_name);

    getPidByName(&pid, "java");
    //printf("getPidByName:%d\n", pid);
    //sleep(15);
}




