/*File name:file.c
 *
 *Author : Xia Dong
 *
 *Copyright all reserved 2013-2014
 *
 *The functions about file management in RaspCloud.
 */

#include <stdio.h>
#include <string.h>
#include <time.h>
/*POSIX header*/
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <fcntl.h>
#include <unistd.h>

#include "../include/marco.h"
#include "../include/file.h"

//char cur_path[MSTRLEN]="/cloud/";	 //Current path in software.交给Python类来维护

void list_file(char *file_list, char *cur_path)
{
	/*Display the file in directory*/
    strcpy(file_list,"");

    DIR *dir = opendir(cur_path);
    
    if(dir == NULL)
    {
        fprintf(stderr,"LIST:Can not open directory %s.\n",cur_path);
        return;
    }
    
    struct dirent *tmp;
    
    while(tmp = readdir(dir))
    {
        strcat(file_list,tmp->d_name);
        strcat(file_list,"\t");
        if(tmp->d_type == DT_DIR)
            strcat(file_list,"dir");
        else if(tmp->d_type == DT_REG)
        	strcat(file_list,"file");
        strcat(file_list,"\n");
    }
    
    closedir(dir);
}

bool new_file(const char *name, char *cur_path)
{
	/*Create a new file*/
    char tmp[MSTRLEN]={0};
    strcat(tmp,cur_path);
    strcat(tmp,name);
    if(creat(tmp,S_IWUSR|S_IRUSR) == -1)
    {
        fprintf(stderr,"NEWFILE:Can not create file %s.\n",name);
        return false;
    }
    else
        return true;
}

bool new_dir(const char *name, char *cur_path)
{
    /*Create a new directory*/

    char tmp[MSTRLEN]={0};
    strcat(tmp,cur_path);
    strcat(tmp,name);
    if(mkdir(tmp,S_IWUSR|S_IRUSR|S_IXUSR) == -1)
    {
        fprintf(stderr,"NEWDIR:Can not create directory %s.\n",name);
        return false;
    }
    else
        return true;
}

bool enter_dir(const char *name, char *cur_path)
{
    /*Enter a directory*/
    char tmp[MSTRLEN]={0};
    strcat(tmp,cur_path);
    strcat(tmp,name);

    if(opendir(tmp) == NULL)
    {
        fprintf(stderr,"ENTERDIR:Can not enter directory %s.\n",name);
        return false;
    }
    else
    {
        strcat(cur_path,name);
        strcat(cur_path,"/");
        return true;
    }
}

bool exit_dir(char *cur_path)
{
    /*Exit to parent directory*/
    if(strlen(cur_path) <= strlen("/cloud/"))
    {
        fprintf(stderr,"EXITDIR:\n");
        return false;
    }
    else
    {
        int i;
        for(i=strlen(cur_path) - 2;i >= 0;i--)
        {
            if(cur_path[i] == '/')
            {
                cur_path[i + 1] = 0;
                return true;
            }
        }
        fprintf(stderr,"EXITDIR:\n");
    }
}

bool del_file(const char *name, char *cur_path)
{
   /*Delete a file,*/
    char tmp[MSTRLEN] = {0};
    strcat(tmp,cur_path);
    strcat(tmp,name);
    if( remove( tmp ) == -1 )
    {
        fprintf(stderr,"DELFILE:Can not delete file, please make sure you have authority\n");
        return false;
    } 
    else
    {
        return true;
    }
}

bool del_dir(const char *name, char *cur_path)
{
    /*Delete a directory,*/
    char tmp[MSTRLEN] = {0};
    strcat(tmp,cur_path);
    strcat(tmp,name);
    if( remove( tmp ) == -1 )
    {
        fprintf(stderr,"DELDIR:Can not delete directory, please make sure you have authority\n");
        return false;
    } 
    else
    {
        return true;
    }

}

void get_dir(char *target, char *cur_path)
{
    /*Get current directory path*/
    strcpy(target,cur_path);
}

void set_dir(char *src, char *cur_path)
{
    /*Set current directory path*/
    strcpy(cur_path,src);
}

long long get_file_size(char *name, char *cur_path)
{
    /*Get the size of file*/
    struct stat buf;
    char tmp[MSTRLEN] = {0};
    strcat(tmp,cur_path);
    strcat(tmp,name);
    stat(tmp,&buf);
    return buf.st_size;
}

time_t get_file_change_time(char *name, char *cur_path)
{
    /*Get file last changed time*/
    struct stat buf;
    char tmp[MSTRLEN] = {0};
    strcat(tmp,cur_path);
    strcat(tmp,name);
    stat(tmp,&buf);
    return buf.st_ctime;
}
