#!/usr/bin/python3

import boto3
import sys


instanceTag = "Horne"
ec2 = boto3.resource('ec2')



def get_command_input(argumentList):
    if len(argumentList) <= 1 or len(argumentList) > 2:
        help()
    elif argumentList[1] in ('start','Start'):
        start_instance()
    elif argumentList[1] in ('stop','Stop'):
        stop_instance()
    elif argumentList[1] in ('status','Status'):
        pass
    elif argumentList[1] in ('terminate','Terminate'):
        pass


def help():
    print("""\
    This is the help function
    will add text later.
    """)

def start_instance():
    print("starting instance")
    

def stop_instance():
    ptint("Stopping instance")



get_command_input(sys.argv)

#print("Number of Arguments:",len(sys.argv), "arguments")
#print("Argument List:", str(sys.argv))



