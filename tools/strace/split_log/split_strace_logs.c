#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>


#define BUFFER_SIZE 128
#define time_window 20
#define FNAME "./strace_logs/%d/%s.log"
#define DNAME "./strace_logs/%d/"
#define DELTA_S 20

char cur_file_name[128];
char cur_dir_name[128];


int main(int argc, const char **argv) {

    char *output_string = (char*)malloc(BUFFER_SIZE);
    unsigned int current_log = 0;
    struct stat st = {0};

    //create the first logging directory
    snprintf(cur_dir_name, 128, DNAME, current_log);

    if (stat(cur_dir_name, &st) == -1) {
        mkdir(cur_dir_name, 0700);
    }

    //create the first log file
    snprintf(cur_file_name, 128, FNAME, current_log, argv[1]);
    FILE *fp = fopen(cur_file_name, "wb");

    //print error if the file does not exist
    if (fp == NULL){
//        printf("Error opening the file %s", cur_file_name);
        return -1;
    }

    long t = time(NULL);
    while(1){
        fgets(output_string, BUFFER_SIZE, stdin);
        fprintf(fp, "%s", output_string);
        fflush(fp);
        if(time(NULL) - t >= DELTA_S){
            ++current_log;
            fclose(fp);

            snprintf(cur_dir_name, 128, DNAME, current_log);
            if (stat(cur_dir_name, &st) == -1) {
                mkdir(cur_dir_name, 0700);
            }

            snprintf(cur_file_name, 128, FNAME, current_log, argv[1]);
            fp = fopen(cur_file_name, "w");
            t = time(NULL);
        }
    }
    
    // close the file
    fclose(fp);
    free(output_string);
    return 0;
}
