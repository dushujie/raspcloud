#! /bin/python
#coding=utf-8
import ctypes, os
MAXN = 10240

class rasp_file:
    def __init__(self, cur_path):
        self.so = ctypes.CDLL("/home/pi/RaspCloud/bin/librcfile.so")
        self.cur_path = cur_path
        self.path = ctypes.create_string_buffer(MAXN)
        self.path.value = self.cur_path

    def list_file(self):
        fun = self.so.list_file
        string = ctypes.create_string_buffer(MAXN)
        fun(string, self.path)
        return string.value


    def new_file(self,name):
        fun = self.o.new_file
        string = ctypes.create_string_buffer(MAXN)
        string.value = name
        re = fun(string,self.path)
        return re


    def new_dir(self,name):
        fun = self.so.new_dir
        string = ctypes.create_string_buffer(MAXN)
        string.value = name
        re = fun(string, self.path)
        return re


    def enter_dir(self,name):
        fun = self.so.enter_dir
        string = ctypes.create_string_buffer(MAXN)
        string.value = name
        re = fun(string, self.path)
        if re == 1:
            self.cur_path = self.cur_path + name
            if self.cur_path[-1] != '/':
                self.cur_path += '/'
            self.path.value = self.cur_path


    def exit_dir(self):
        fun = self.so.exit_dir
        re = fun(self.path)
        if re == 1:
            if len(self.path.value) > len('/cloud/'):
                self.cur_path = self.path.value
                return 1
            self.path.value = self.cur_path
            return 0
        else:
            self.path.value = self.cur_path
            return 0


    def del_file(self,name):
        fun = self.so.del_file
        string = ctypes.create_string_buffer(MAXN)
        string.value = name
        re = fun(string, self.path)
        return re


    def del_dir(self,name):
        fun = self.so.del_dir
        string = ctypes.create_string_buffer(MAXN)
        string.value = name
        re = fun(string,self.path)
        return re

    def get_dir(self):
        return self.cur_path

    def set_dir(self,string):
        self.cur_path = string
        self.path.value = string

    def get_file_size(self,name):
        fun = self.so.get_file_size
        string = ctypes.create_string_buffer(MAXN)
        string.value = name
        re = fun(string, self.path)
        return re

    def get_file_change_time(self,name):
        fun = self.so.get_file_change_time
        string = ctypes.create_string_buffer(MAXN)
        string.value = name
        re = fun(string, self.path)
        return re