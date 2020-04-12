import boto3

class Ec2Control():
    def create_instance(num):
        ec2 = boto3.resource('ec2')
        instance = ec2.create_instances(
            MaxCount=num,
            MinCount=num,
            ImageId='ami-01288945bd24ed49a',
            InstanceType='t2.micro',
            SecurityGroupIds=[
                'sg-e6c67b86',
            ],
            InstanceInitiatedShutdownBehavior='terminate',
            KeyName='homekey_desktop',
            UserData='''
                    #!/bin/bash
                    sudo echo password | passwd root --stdin
                    sudo yum install -y amazon-efs-utils dialog
                    sudo mkdir /mnt/efs
                    sudo mount -t efs fs-a75412c6:/ /mnt/efs
                    sudo sed -i "s/PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config
                    sudo systemctl restart sshd
                    '''
        )
        return instance

    def list_instance():
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances()
        for i in response['Reservations']:
            for instance in i['Instances']:
                print("+++++++++++++++++++++++++++++++++++")
                print("InstanceId: " + instance['InstanceId'])
                print("State: " + instance['State']['Name'])
                if instance['State']['Name'] != 'terminated':
                    print("PublicIP: " + instance["PublicIpAddress"])
                    print("PrivateIP: " + instance["PrivateIpAddress"])
