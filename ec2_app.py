#!/usr/bin/python3

#Import required librarys.
import boto3
import sys

#Set instance tag and instantiate ec2 boto resource.
#To change instace name tag, edit the line below.
instanceTag = "horne"
instanceType = "t2.nano"
imageID = "ami-31490d51"

ec2 = boto3.resource('ec2')

def get_command_input(argumentList):
    """Call method as requested from comand line.
    
    If a sting is found that matches input the arguement, the associated method 
    is called. If the list contains no areguments or unknown argiments, help 
    information is printed
    """
    if len(argumentList) < 2:
        #if there a no arguments, show help
        help()
    elif argumentList[1] in ('start','Start'):
        start_instance()
    elif argumentList[1] in ('stop','Stop'):
        stop_instance()
    elif argumentList[1] in ('status','Status'):
        instance_status()
    elif argumentList[1] in ('terminate','Terminate'):
        terminate_instance()
    else:
        #Show help if argument is undefined.
        help()

def help():
    """Help Desctiption
    
    Prints example commands and their description to screen.
    """
    print("""\
    Command line examples:
    
    Start
    Check if an instance exists, if it does and is not running, start the instance. 
    If no instance is found or it has a state of terminated, this will create a new in
    stance and tag it with the name tag set to the value of the variable 'instanceTag'    with in this script.
    
    example: python ec2_app.py start

    Stop
    Check if there is a running instance with the name tag set in variable 
    'instanceTag', if found it will stop this instance, else it will do nothing.

    example: python ec2_app.py stop

    Status
    Check for an instance with the name tag set in variable 'instanceTag' if found 
    print its status to screen.

    example: python ec2_app.py status

    Terminate
    Check for any instance with the name tag set in variable 'instancetag' that does 
    not have its state set to terminated and terminate the instance.

    example: python ec2_app.pt terminate
     """)

def start_instance():
    """Find and start instance or create new instance.

    Find instance to start, if no instance is found create a new instance. if found
    instance is in an intermediate state no action is taklen.
    """
    print("Locating instance to start")
    foundInstance = find_instance(instanceTag,'pending','running','shutting-down',
                                  'stopping','stopped')
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
    """Find instance to terminate.

    Locate instance in any state that is not terminated and terminate the instance.
    """
    print('Locating instance to terminate')
    instanceToTerminate = find_instance(instanceTag, 'pending','running',
                                        'shutting-down','stopping','stopped')
    if instanceToTerminate is None:
        print('All instances already terminated.')
    else:
        print('Terminating instance', instanceToTerminate.id)
        instanceToTerminate.terminate()

def instance_status():
    """Get state of instance.

    Locate instance and print its state.
    """
    print('Gettng instance status')
    instance = find_instance(instanceTag, 'pending','running','shutting-down',
                             'stopping','stopped')
    if instance is None:
        print('Instance is terminated or no instances exist to show their current', 
              'status.')
    else:
        instance.load()
        print('Currently managed instance', instance.id, 'status is' , instance.state['Name'])
        

def stop_instance():
    """Stop instance.
    
    Locate instance in runnind or pending state and stop the instance.
    """
    print('Locating instance to stop')
    instanceToStop = find_instance(instanceTag, 'pending', 'running')
    if instanceToStop is None:
        print('No running or pending instances to stop.')
    else:
        print('Stoppping instance', instanceToStop.id)
        instanceToStop.stop()

def make_new_Instance(tagForNewInstance):
    """Create a new instance and tag.

    Creates a new instance from the specified input and once created tages with 
    specified name tag. 
    """
    [newInstance] = ec2.create_instances(ImageId=imageID, 
                                         InstanceType=instanceType, MinCount=1, 
                                         MaxCount=1)
    newInstance.create_tags(Tags=[{'Key': 'Name','Value': tagForNewInstance}])
    print('Created new instance with id', newInstance.id, 'and gave a Name tag of', 
          tagForNewInstance,'.')

def find_instance(tagName, *instanceStates):
    """Worker method, finds and returns instance.

    Finds instance with specified name tag and instance state specified and returns 
    the fist instance that matches.
    """
    listOfInstances = list(ec2.instances.filter(Filters=[{'Name':'tag:Name',
                                                'Values':[tagName]}]))
    if len(listOfInstances) > 0:
        print('Found the folowing instances with the tag', tagName)
    returnInstance = None
    for instance in listOfInstances:
        print('Instance id',instance.id,'in', instance.state['Name'], 'state.')
        if instance.state['Name'] in instanceStates:
            returnInstance = instance  
    return returnInstance

#Set entry point into script, and also allow code to be resued in other modules.
if __name__ == "__main__":
    get_command_input(sys.argv)

