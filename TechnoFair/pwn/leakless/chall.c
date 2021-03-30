#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <seccomp.h>
#include <sys/mman.h>


struct item{
    char *msg;
};

struct item ptr[0x90] = {0};

// gcc chall.c -o chall -m64 -no-pie -lseccomp -fstack-protector-all
int pos;

void menu() {
  puts("\t    __           __   __");
  puts("\t   / /__  ____ _/ /__/ /__  __________");
  puts("\t  / / _ \\/ __ `/ //_/ / _ \\/ ___/ ___/");
  puts("\t / /  __/ /_/ / ,< / /  __(__  |__  )");
  puts("\t/_/\\___/\\__,_/_/|_/_/\\___/____/____/");
}

void choicemenu() {
        printf("\n1. create\n2. delete\n3. exit\n\n> ");
}

void create() {
  char sizebuf[0x10];
  int size;
        if(pos < 0x90) {
                printf("[?] size : ");
                read(0,sizebuf,0x10);
                size = atoi(sizebuf);
                if(size <= 0) {
                        puts("[x] invalid size");
                } else {
                        ptr[pos].msg = (char*)malloc(size);
                        printf("[?] msg : ");
                        read(0,ptr[pos].msg,size);
                        pos++;
                        puts("[+] success");
                }
        } else {
                puts("[!] resource full");
        }
}

void delete() {
        char indexbuf[0x10];
        int index;
        if(!pos) {
                puts("[x] empty");
                return 0;
        } else {
                printf("[?] idx : ");
                read(0,indexbuf,0x10);
                index = atoi(indexbuf);
                if(ptr[index].msg) {
                        free(ptr[index].msg);
                        puts("[+] success");
                } else {
                        puts("[x] failed");
                }
        }
}

void init() {
  setvbuf(stdout, 0 , 2 , 0);
  setvbuf(stdin, 0 , 2 , 0);
  scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
  seccomp_rule_add(ctx,SCMP_ACT_KILL,SCMP_SYS(execve),0);
  seccomp_rule_add(ctx,SCMP_ACT_KILL,SCMP_SYS(execveat),0);
  seccomp_load(ctx);
}

void main() {
  char choicebuf[0x10];
  int choice;
  init();
  menu();
  while(1) {
      choicemenu();
      read(0,choicebuf,0x10);
      choice = atoi(choicebuf);
      switch(choice) {
          case 1:
          create();
          break;
          case 2:
          delete();
          break;
          case 3:
          exit(0);
          break;
          default:
          puts("[!] try again");
          break;
        }
    }
}
