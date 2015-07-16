/*Copyright 2013-2014
 *
 *All rights reserved.
 *
 *Name:file.h
 *Author:XiaDong
 *E-mail:xiadong1994@126.com 
 *Date:2014-4-22
 */

#ifndef _H_RASPCLOUDFILE
#define _H_RASPCLOUDFILE

#include "marco.h"

/*Display the file in directory*/
void list_file(char *file_list, char *cur_path);

/*Create a new file*/
bool new_file(const char *name, char *cur_path);

/*Create a new directory*/
bool new_dir(const char *name, char *cur_path);

/*Enter a directory*/
bool enter_dir(const char *name, char *cur_path);

 /*Exit to parent directory*/
bool exit_dir(char *cur_path);

/*Delete a file*/
bool del_file(const char *name, char *cur_path);

/*Delete a directory*/
bool del_dir(const char *name, char *cur_path);

/*Get current directory path*/
void get_dir(char *target, char *cur_path);

/*Set current directory path*/
void set_dir(char *src, char *cur_path);

/*Get the size of file*/
long long get_file_size(char *name, char *cur_path);

/*Get file last changed time*/
time_t get_file_change_time(char *name, char *cur_path);
#endif
