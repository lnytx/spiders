# -*- coding: utf-8 -*-

'''
Created on 2011-8-24
主要用途：
    对程序中所使用的loggong模式做一般性配置
     日志处理
'''

import logging

import logging.handlers

import os
def log():
#     LEVELS = {'NOSET': logging.NOTSET,
#               'DEBUG': logging.DEBUG,
#               'INFO': logging.INFO,
#               'WARNING': logging.WARNING,
#               'ERROR': logging.ERROR,
#               'CRITICAL': logging.CRITICAL}
    
    #set up logging to file
    
    #logging.basicConfig(level = logging.NOTSET,
    #                    format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    #                    )
    
    ##                    filename = "./log.txt",
    
    ##                    filemode = "w")
    
    # create logs file folder
    base_dir='D:\Program Files\Python_Workspace\log_files'
    logs_dir = os.path.join(base_dir, "logs")
    file_name=logs_dir+'\log.txt'
    print("file_name",file_name)
    print("logs_dir",logs_dir)
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.mkdir(logs_dir)
      
    # define a rotating file handler
    #滚动时写入，按大小写入，每个50M
    #rotatingFileHandler = logging.handlers.RotatingFileHandler(filename =file_name,maxBytes = 1024 * 1024 * 50,backupCount = 5)
    #按日期写入
    rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(file_name,when='M',interval=1,backupCount=40)
    
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    
    rotatingFileHandler.setFormatter(formatter)
    
    logging.getLogger("").addHandler(rotatingFileHandler)
    
    #define a handler whitch writes messages to sys
    #控制台输出
    console = logging.StreamHandler()
    
    console.setLevel(logging.NOTSET)
    
    #set a format which is simple for console use
    
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    #formatter = logging.Formatter("%(name)s: %(levelname)s %(message)s")
    
    #tell the handler to use this format
    
    console.setFormatter(formatter)
    
    #add the handler to the root logger
    
    logging.getLogger("").addHandler(console)
    
    # set initial log level
    logger = logging.getLogger("")
    logger.setLevel(logging.NOTSET)  
    return logger


if __name__ == "__main__":
    msg = "this is just a test"
    log=log()
    log.info(msg)
    log.error(msg)
    log.debug(msg)
    #log.WARNING(msg)
    #log.NOTSET(msg)