#!/usr/bin/python3

import boto3
import sys


instanceTag = "horne"
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
    foundInstance = find_instance_id(instanceTag)
    if foundInstance.state['Name'] == 'terminated':
        make_new_Instance(instanceTag)
    elif foundInstance.state['Name'] == 'stopped':
        foundInstance.start()
    
    
   # foundInstance.wait_until_running()
    
    

def stop_instance():
    ptint("Stopping instance")

def make_new_Instance(tagForNewInstance):
    [newInstance] = ec2.create_instances(ImageId='ami-83da9ce3', InstanceType='t1.micro', MinCount=1, MaxCount=1)
    print(tagForNewInstance)

def find_instance_id(tagName):
    listOfInstances = list(ec2.instances.filter(Filters=[{'Name':'tag:Name','Values':[tagName]}]))
    if len(listOfInstances) == 1:
        return listOfInstances[0]

    




get_command_input(sys.argv)

#print("Number of Arguments:",len(sys.argv), "arguments")
#print("Argument List:", str(sys.argv))



