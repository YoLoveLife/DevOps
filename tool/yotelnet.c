#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <memory.h>
#include <stdio.h>
#include <errno.h>
#define TIMEOUT 5
int main(int argc,char *argv[]){
	int sock;
	int port;
	char* address;
	if(argc!=3){
		printf("Usage: %s address port\n",argv[0]);
		return 0;
	}
	
	address = argv[1];
	port = atoi(argv[2]);

	sock = socket(AF_INET,SOCK_STREAM,0);
	if(sock == -1){
		printf("False");
		return 0;
	}

	struct sockaddr_in dst;
    struct hostent *h;

	h = gethostbyname(address);
	if(h==NULL){
        printf("False");
        return 0;
	}
	else{
        memcpy(&dst.sin_addr.s_addr,h->h_addr,4);
	}

//	dst.sin_addr.s_addr = inet_addr(address);
	dst.sin_family = AF_INET;
	dst.sin_port = htons(port);


	if(connect(sock,(struct sockaddr *)&dst,sizeof(dst))<0){
	//	perror("Connect failed.Error");
		printf("False");
		exit(0);
	}else{
		printf("True");
		exit(0);
	}
}
