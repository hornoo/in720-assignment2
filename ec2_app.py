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
        instance_status()
    elif argumentList[1] in ('terminate','Terminate'):
        terminate_instance()

def help():
    print("""\
    This is the help function
    will add text later.
    """)

def start_instance():
    print("Locating instance to start")
    foundInstance = find_instance(instanceTag,'pending','running','shutting-down','stopping','stopped')
    #print(foundInstance)
    if foundInstance is None:
        print('No instance found to start')
        make_new_Instance(instanceTag)
    elif foundInstance.state['Name'] == 'stopped':
        print('Found stopped instance, starting', foundInstance.id, )
        foundInstance.start()
    else:
        print(foundInstance.id,'found',foundInstance.state['Name'],', no action taken.')
    
def terminate_instance():
    print('Locating instance to terminate')
    instanceToTerminate = find_instance(instanceTag, 'pending','running','shutting-down','stopping','stopped')
    if instanceToTerminate is None:
        print('All instances already terminated.')
    else:
        print('Terminating instance', instanceToTerminate.id)
        instanceToTerminate.terminate()

def instance_status():
    print('Gettng instance status')
    instance = find_instance(instanceTag, 'pending','running','shutting-down','stopping','stopped')
    if instance is None:
        print('Instance is terminated or no instances exist')
    else:
        instance.load()
        print('Instance', instance.id, 'status' , instance.state['Name'])
        

def stop_instance():
    print('Locating instance to stop')
    instanceToStop = find_instance(instanceTag, 'pending', 'running')
    if instanceToStop is None:
        print('No running or pending instances to stop.')
    else:
        print('Stoppping instance', instanceToStop.id)
        instanceToStop.stop()

def make_new_Instance(tagForNewInstance):
    [newInstance] = ec2.create_instances(ImageId='ami-31490d51', InstanceType='t2.nano', MinCount=1, MaxCount=1)
    newInstance.create_tags(Tags=[{'Key': 'Name','Value': tagForNewInstance}])
    print('Created new instance with id', newInstance.id, 'and gave a Name tag of', tagForNewInstance,'.')

def find_instance(tagName, *instanceStates):
    listOfInstances = list(ec2.instances.filter(Filters=[{'Name':'tag:Name','Values':[tagName]}]))
    print('Found the folowing instances with the tag', tagName)
    returnInstance = None
    for instance in listOfInstances:
        print('Instance id',instance.id,'in', instance.state['Name'], 'state.')
        if instance.state['Name'] in instanceStates:
            returnInstance = instance 
    print('Returning', returnInstance.id)    
    return returnInstance


get_command_input(sys.argv)

