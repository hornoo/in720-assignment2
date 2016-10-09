# in720-assignment2


##ec2_app

This a a basic brogram that can be used to start, stop, terminate and get the status of an aws ec2 instance specified by a tag.

###Requirements:

python 3.5

awscli

###setup: 
Insure python 3.5 and the AWS commanline interface are installed, once installed you need to set up your aws authentication details.

If you have the AWS CLI installed, then you can use it to configure your credentials file:

aws configure

Alternatively, you can create the credential file yourself. By default, its location is at ~/.aws/credentials:

[default]

aws_access_key_id = YOUR_ACCESS_KEY

aws_secret_access_key = YOUR_SECRET_KEY

You may also want to set a default region. This can be done in the configuration file. By default, its location is at ~/.aws/config:

[default]
region= us-west-1


Install boto3 by running

  python pip install -r requirements.txt

To set your instance tag, open ec2_app.py in a text editor and change the value stored in the variable 'instanceTag'.


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
