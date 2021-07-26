#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>


#define BUFFER_SIZE 128
#define time_window 20
#define FNAME "%s_%d.txt"
#define DELTA_S 20

char cur_file_name[128];

int main(int argc, const char **argv) {

    char *output_string = (char*)malloc(BUFFER_SIZE);
    unsigned int current_file = 0;

    snprintf(cur_file_name, 128, FNAME, argv[1], current_file);
    FILE *fp = fopen(cur_file_name, "wb");

    //print error if the file does not exist
    if (fp == NULL){
        printf("Error opening the file %s", cur_file_name);
        return -1;
    }

    long t = time(NULL);
    while(1){
        fgets(output_string, BUFFER_SIZE, stdin);
        fprintf(fp, "%s", output_string);
        fflush(fp);
        if(time(NULL) - t >= DELTA_S){
            ++current_file;
            fclose(fp);
            snprintf(cur_file_name, 128, FNAME, argv[1], current_file);
            fp = fopen(cur_file_name, "w");
            t = time(NULL);
        }
    }
    
    // close the file
    fclose(fp);
    free(output_string);
    return 0;
}
