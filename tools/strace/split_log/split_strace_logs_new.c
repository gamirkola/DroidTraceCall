#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include<dirent.h>
#include<string.h>

#define BUFFER_SIZE 128
#define time_window 20
#define FNAME "./strace_logs/%d/%s.log"
#define DNAME "./strace_logs/%d/"
#define INDEX "./time_window_index/index"

char cur_file_name[128];
char cur_dir_name[128];

int main(int argc, const char **argv) {

    char *output_string = (char*)malloc(BUFFER_SIZE);
    struct stat st = {0};
    FILE *fileStream;
    int current_log;
    char i[2];

    fileStream = fopen(INDEX, "r");
    fgets(i,2,fileStream);
    fclose(fileStream);
    current_log = atoi(i);

    //create fisrt dir
    snprintf(cur_dir_name, 128, DNAME, current_log);

    if (stat(cur_dir_name, &st) == -1) {
        mkdir(cur_dir_name, 0777);
    }

    //create the first log file
    snprintf(cur_file_name, 128, FNAME, current_log, argv[1]);
    FILE *fp = fopen(cur_file_name, "wb");

    //print error if the file does not exist
    if (fp == NULL){
        return -1;
    }

    while(1){
        fgets(output_string, BUFFER_SIZE, stdin);
        fprintf(fp, "%s", output_string);
        fflush(fp);
        fileStream = fopen(INDEX, "r");
        fgets(i,2,fileStream);
        fclose(fileStream);
        if(current_log < atoi(i)){
            fclose(fp);
            current_log = atoi(i);

            snprintf(cur_dir_name, 128, DNAME, current_log);
            if (stat(cur_dir_name, &st) == -1) {
                mkdir(cur_dir_name, 0777);
            }

            snprintf(cur_file_name, 128, FNAME, current_log, argv[1]);
            fp = fopen(cur_file_name, "w");
        }
    }

    fclose(fp);
    fclose(fileStream);
    free(output_string);
    return 0;

}
