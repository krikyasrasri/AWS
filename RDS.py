import boto3
import sys
import fnmatch
import random
import urllib
from html.parser import HTMLParser
import json
import requests

#print the script name
#print(sys.argv[0])

#print the 1st argiment which is VPC ID
#print("As VPC ID : %s" %(sys.argv[1]))

#v_VPCID=sys.argv[1]

def get_subnet(v_VPCID):
    v_EC2=boto3.client('ec2')
    v_SUBNET_DICT = v_EC2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [v_VPCID]}])
    v_LEN = len(v_SUBNET_DICT['Subnets'])
    datasubnetlist=[]
    if v_LEN < 1 :
        print("ERROR : SUBNET Information is not available. Check the AWS stack")

    print('Length : %d' % len(v_SUBNET_DICT['Subnets']))

    for count in range(0,v_LEN):
        #print("%d : %s " % (count, v_SUBNET_DICT['Subnets'][count]['SubnetId']))
        v_taglen=len(v_SUBNET_DICT['Subnets'][count]['Tags'])

        for tagcount in range(0,v_taglen):
            #print(tagcount)
            if v_SUBNET_DICT['Subnets'][count]['Tags'][tagcount]['Key'] == 'Name':
                if fnmatch.fnmatch(v_SUBNET_DICT['Subnets'][count]['Tags'][tagcount]['Value'],'DataSubnetAz[1-3]'):
                    print("%s - %s "  % (v_SUBNET_DICT['Subnets'][count]['Tags'][tagcount]['Value'],v_SUBNET_DICT['Subnets'][count]['SubnetId']))
                    #print(v_SUBNET_DICT['Subnets'][count]['SubnetId'])
                    datasubnetlist.append(v_SUBNET_DICT['Subnets'][count]['SubnetId'])
                #print(v_SUBNET_DICT['Subnets'][count]['Tags'][tagcount]['Value'])

            #print(v_SUBNET_DICT['Subnets'][count]['Tags'][tagcount])
        #print(v_SUBNET_DICT['Subnets'][count]['Tags'][4]['Value'])

    #print(v_SUBNET_DICT['Subnets'][count]['SubnetId']['Tags'][4]['Value'])
    return datasubnetlist

def get_vpcid():
    v_ec2 = boto3.client('ec2')
    v_vpc = v_ec2.describe_vpcs()
    v_vpc_len = len(v_vpc['Vpcs'])
    v_vpc_dict={}
    print(v_vpc_len)
    if v_vpc_len > 1:
        print("Following VPC-IDs are available")
        for i in range(0, v_vpc_len):
            v_taglen=len(v_vpc['Vpcs'][i]['Tags'])
            for j in range(0,v_taglen):
                if v_vpc['Vpcs'][i]['Tags'][j]['Key'] == 'Name':
                    v_vpc_dict[v_vpc['Vpcs'][i]['Tags'][j]['Value']]=v_vpc['Vpcs'][i]['VpcId']
        for key,value in v_vpc_dict.items():
            print("%s" %(key))
        v_vpc_id=input("Enter the VPC-ID : ")
        return v_vpc_dict[v_vpc_id]
    else:
        return v_vpc['Vpcs'][0]['VpcId']


def get_rdsinput():
    v_rdslist = ['aurora', 'mysql', 'oracle-ee', 'sqlserver-ee']
    print("RDS Engines available for AWS RDS Offering :-")
    for rdbms in v_rdslist:
        print("%d) %s " % (v_rdslist.index(rdbms), rdbms))
    v_rdbms=v_rdslist[int(input("Enter the required RDS engine : "))]
    v_engver=0

    if v_rdbms == 'mysql' or v_rdbms == 'aurora':
        v_engver=input("Enter version 5.6/5.7 : ")
    if v_rdbms == 'oracle-ee':
        v_engver=input("Enter version 11.2/12.1 : ")



    print("RDS Compue Class (https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html) Default is db.t2.medium")
    #v_rdscom=input("Enter RDS Compute class : ")

    # offers = requests.get(
    #     'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json'
    # )
    # ec2_offer_path = offers.json()['offers']['AmazonRDS']['currentVersionUrl']
    # ec2offer = requests.get(
    #     'https://pricing.us-east-1.amazonaws.com%s' % ec2_offer_path
    # ).json()
    #
    # rds_comp_list = []
    # for sku, data in ec2offer['products'].items():
    #     if data['productFamily'] != 'Database Instance':
    #         # skip anything that's not an DB Instance
    #         continue
    #     if data['attributes']['location'] == 'US West (Oregon)':
    #         rds_comp_list.append(data['attributes']['instanceType'])

    rds_comp_list=['db.t2.small', 'db.m4.large', 'db.m1.large', 'db.t2.medium', 'db.r3.large', 'db.m3.xlarge', 'db.m1.small',
     'db.m1.xlarge', 'db.r4.4xlarge', 'db.t2.large', 'db.m1.small', 'db.t2.medium', 'db.t2.large', 'db.m4.large',
     'db.t2.small', 'db.t2.medium', 'db.m2.xlarge', 'db.m4.16xlarge', 'db.r3.4xlarge', 'db.r4.xlarge', 'db.r3.4xlarge',
     'db.r3.xlarge', 'db.t2.large', 'db.r4.xlarge', 'db.r4.16xlarge', 'db.m1.xlarge', 'db.r4.8xlarge', 'db.m4.large',
     'db.r4.xlarge', 'db.r4.4xlarge', 'db.m2.2xlarge', 'db.t1.micro', 'db.m4.2xlarge', 'db.m3.large', 'db.m4.2xlarge',
     'db.r3.large', 'db.r4.8xlarge', 'db.r3.large', 'db.t2.small', 'db.t2.2xlarge', 'db.m4.xlarge', 'db.m2.4xlarge',
     'db.m3.2xlarge', 'db.r4.8xlarge', 'db.m3.2xlarge', 'db.m1.large', 'db.m1.small', 'db.m4.2xlarge', 'db.t2.small',
     'db.m4.2xlarge', 'db.t2.small', 'db.r4.2xlarge', 'db.t2.micro', 'db.r3.large', 'db.r3.large', 'db.m1.medium',
     'db.r4.xlarge', 'db.m2.4xlarge', 'db.m4.large', 'db.t2.2xlarge', 'db.r4.large', 'db.m4.16xlarge', 'db.m2.2xlarge',
     'db.r4.16xlarge', 'db.r3.2xlarge', 'db.m4.16xlarge', 'db.m1.medium', 'db.m2.4xlarge', 'db.m2.4xlarge',
     'db.r4.2xlarge', 'db.m1.large', 'db.t2.medium', 'db.m4.large', 'db.m1.large', 'db.r4.2xlarge', 'db.r4.xlarge',
     'db.r4.xlarge', 'db.r4.xlarge', 'db.m4.10xlarge', 'db.r3.xlarge', 'db.r4.2xlarge', 'db.m4.2xlarge',
     'db.m2.2xlarge', 'db.m2.xlarge', 'db.t2.xlarge', 'db.r3.8xlarge', 'db.t2.micro', 'db.r4.2xlarge', 'db.t2.medium',
     'db.r3.8xlarge', 'db.r4.4xlarge', 'db.t2.large', 'db.t2.medium', 'db.m2.xlarge', 'db.m2.2xlarge', 'db.m3.large',
     'db.m4.large', 'db.m3.medium', 'db.m1.small', 'db.r4.xlarge', 'db.r3.xlarge', 'db.r4.8xlarge', 'db.t1.micro',
     'db.m4.4xlarge', 'db.m2.4xlarge', 'db.m3.2xlarge', 'db.r3.xlarge', 'db.r3.xlarge', 'db.m4.16xlarge',
     'db.m3.2xlarge', 'db.m4.xlarge', 'db.t2.small', 'db.r3.8xlarge', 'db.m2.4xlarge', 'db.m3.medium', 'db.t2.medium',
     'db.m4.xlarge', 'db.m1.xlarge', 'db.t2.2xlarge', 'db.t2.small', 'db.m1.large', 'db.m2.4xlarge', 'db.r3.2xlarge',
     'db.t2.micro', 'db.m3.large', 'db.r4.16xlarge', 'db.t2.micro', 'db.t2.small', 'db.r4.large', 'db.m4.16xlarge',
     'db.r4.large', 'db.m3.large', 'db.r4.8xlarge', 'db.m4.xlarge', 'db.t2.large', 'db.m4.4xlarge', 'db.m3.2xlarge',
     'db.m4.large', 'db.t2.large', 'db.t2.micro', 'db.r4.4xlarge', 'db.m2.xlarge', 'db.t2.large', 'db.r3.4xlarge',
     'db.m3.large', 'db.t1.micro', 'db.m3.2xlarge', 'db.r4.2xlarge', 'db.r4.xlarge', 'db.m4.large', 'db.r4.16xlarge',
     'db.m4.10xlarge', 'db.m1.xlarge', 'db.m4.4xlarge', 'db.m2.xlarge', 'db.m2.xlarge', 'db.m3.2xlarge',
     'db.m2.2xlarge', 'db.m1.medium', 'db.r3.large', 'db.r3.2xlarge', 'db.m3.medium', 'db.m4.large', 'db.r4.4xlarge',
     'db.m4.xlarge', 'db.r4.8xlarge', 'db.m3.2xlarge', 'db.t1.micro', 'db.m4.4xlarge', 'db.r4.4xlarge', 'db.r4.xlarge',
     'db.m1.small', 'db.t2.xlarge', 'db.r3.large', 'db.r3.2xlarge', 'db.r4.large', 'db.t2.large', 'db.t1.micro',
     'db.t2.medium', 'db.m4.16xlarge', 'db.m4.16xlarge', 'db.m2.xlarge', 'db.m1.large', 'db.m1.small', 'db.r3.8xlarge',
     'db.m3.2xlarge', 'db.r3.large', 'db.m1.large', 'db.t1.micro', 'db.r4.large', 'db.m4.4xlarge', 'db.t2.micro',
     'db.t1.micro', 'db.m4.2xlarge', 'db.r4.xlarge', 'db.m3.medium', 'db.t2.micro', 'db.r4.xlarge', 'db.t2.small',
     'db.r4.large', 'db.r3.2xlarge', 'db.r3.4xlarge', 'db.m3.medium', 'db.m1.xlarge', 'db.m4.xlarge', 'db.t2.xlarge',
     'db.m1.medium', 'db.t2.xlarge', 'db.r3.8xlarge', 'db.r4.4xlarge', 'db.t2.medium', 'db.m2.2xlarge', 'db.m1.xlarge',
     'db.r4.xlarge', 'db.t2.medium', 'db.r3.4xlarge', 'db.r3.xlarge', 'db.r3.4xlarge', 'db.r4.4xlarge', 'db.m3.medium',
     'db.r4.8xlarge', 'db.t2.micro', 'db.m3.2xlarge', 'db.r4.4xlarge', 'db.t2.2xlarge', 'db.m3.xlarge', 'db.m1.large',
     'db.r3.xlarge', 'db.r3.2xlarge', 'db.m3.medium', 'db.r3.large', 'db.m1.medium', 'db.m2.xlarge', 'db.r3.xlarge',
     'db.r4.8xlarge', 'db.m3.large', 'db.m3.medium', 'db.t2.xlarge', 'db.m3.medium', 'db.t2.medium', 'db.m3.large',
     'db.r4.2xlarge', 'db.t2.small', 'db.m4.2xlarge', 'db.r4.8xlarge', 'db.m3.large', 'db.r4.8xlarge', 'db.m3.xlarge',
     'db.m3.large', 'db.m2.xlarge', 'db.t2.xlarge', 'db.r3.2xlarge', 'db.r4.16xlarge', 'db.t2.large', 'db.r3.2xlarge',
     'db.m4.4xlarge', 'db.m4.large', 'db.m3.2xlarge', 'db.m1.medium', 'db.t2.xlarge', 'db.m4.16xlarge', 'db.t2.small',
     'db.m1.medium', 'db.m1.medium', 'db.r3.xlarge', 'db.m3.medium', 'db.r4.4xlarge', 'db.r4.large', 'db.r3.4xlarge',
     'db.r3.2xlarge', 'db.m4.large', 'db.r4.16xlarge', 'db.m4.16xlarge', 'db.m1.small', 'db.t2.large', 'db.r4.xlarge',
     'db.m4.2xlarge', 'db.m3.medium', 'db.m4.4xlarge', 'db.r4.large', 'db.m1.medium', 'db.m1.xlarge', 'db.m2.xlarge',
     'db.r3.large', 'db.m4.4xlarge', 'db.m4.16xlarge', 'db.m3.2xlarge', 'db.t2.medium', 'db.m1.medium', 'db.r3.2xlarge',
     'db.r3.4xlarge', 'db.t2.xlarge', 'db.m2.xlarge', 'db.t2.large', 'db.r3.2xlarge', 'db.m1.xlarge', 'db.m1.xlarge',
     'db.t2.medium', 'db.t2.xlarge', 'db.t2.2xlarge', 'db.r3.xlarge', 'db.m3.medium', 'db.m1.large', 'db.m4.16xlarge',
     'db.m4.2xlarge', 'db.t2.large', 'db.m4.4xlarge', 'db.m3.large', 'db.r4.2xlarge', 'db.m1.small', 'db.m3.medium',
     'db.m4.xlarge', 'db.t2.xlarge', 'db.m2.2xlarge', 'db.t2.xlarge', 'db.r3.xlarge', 'db.m4.2xlarge', 'db.t2.2xlarge',
     'db.m1.medium', 'db.r4.large', 'db.m4.10xlarge', 'db.r4.8xlarge', 'db.m4.4xlarge', 'db.m1.large', 'db.r4.16xlarge',
     'db.m2.2xlarge', 'db.r3.large', 'db.m1.small', 'db.r4.2xlarge', 'db.m2.4xlarge', 'db.r4.4xlarge', 'db.t1.micro',
     'db.r3.4xlarge', 'db.r4.8xlarge', 'db.r3.2xlarge', 'db.m4.2xlarge', 'db.m1.small', 'db.m3.large', 'db.t1.micro',
     'db.r3.xlarge', 'db.m4.large', 'db.r4.xlarge', 'db.r3.2xlarge', 'db.m3.2xlarge', 'db.t2.2xlarge', 'db.t2.small',
     'db.m1.xlarge', 'db.m2.4xlarge', 'db.t2.small', 'db.m2.2xlarge', 'db.r4.xlarge', 'db.m1.large', 'db.r3.8xlarge',
     'db.r3.2xlarge', 'db.r3.4xlarge', 'db.t2.small', 'db.r3.4xlarge', 'db.r3.4xlarge', 'db.m4.large', 'db.m3.xlarge',
     'db.r3.8xlarge', 'db.r3.large', 'db.m3.xlarge', 'db.r4.large', 'db.r4.xlarge', 'db.r4.2xlarge', 'db.m4.2xlarge',
     'db.m2.4xlarge', 'db.t2.large', 'db.r3.2xlarge', 'db.r3.2xlarge', 'db.r3.2xlarge', 'db.r4.xlarge', 'db.r4.2xlarge',
     'db.m4.2xlarge', 'db.r4.xlarge', 'db.m3.medium', 'db.t2.medium', 'db.m1.medium', 'db.m4.xlarge', 'db.m1.xlarge',
     'db.m2.4xlarge', 'db.r3.2xlarge', 'db.m1.xlarge', 'db.m3.xlarge', 'db.m4.4xlarge', 'db.m3.2xlarge',
     'db.r3.4xlarge', 'db.m3.xlarge', 'db.r3.xlarge', 'db.m3.2xlarge', 'db.m4.10xlarge', 'db.r3.4xlarge', 'db.m1.small',
     'db.t2.micro', 'db.r4.8xlarge', 'db.m2.2xlarge', 'db.t2.medium', 'db.r4.4xlarge', 'db.r4.4xlarge',
     'db.m4.16xlarge', 'db.m3.xlarge', 'db.t2.small', 'db.r4.2xlarge', 'db.m3.large', 'db.m4.4xlarge', 'db.m3.large',
     'db.m4.large', 'db.r4.xlarge', 'db.m2.xlarge', 'db.m4.large', 'db.m3.large', 'db.m1.large', 'db.m1.xlarge',
     'db.m3.2xlarge', 'db.m4.4xlarge', 'db.m1.medium', 'db.r4.large', 'db.r4.large', 'db.m4.2xlarge', 'db.r4.xlarge',
     'db.r4.large', 'db.r3.4xlarge', 'db.m4.4xlarge', 'db.m4.xlarge', 'db.m4.4xlarge', 'db.m2.2xlarge', 'db.r4.xlarge',
     'db.m1.large', 'db.m2.4xlarge', 'db.m3.xlarge', 'db.r4.8xlarge', 'db.m1.large', 'db.m3.xlarge', 'db.r4.large',
     'db.t2.large', 'db.m3.xlarge', 'db.m4.4xlarge', 'db.m3.xlarge', 'db.r4.2xlarge', 'db.m4.xlarge', 'db.m4.4xlarge',
     'db.t2.2xlarge', 'db.m2.xlarge', 'db.r4.xlarge', 'db.m1.medium', 'db.t2.medium', 'db.m2.4xlarge', 'db.m1.xlarge',
     'db.r3.xlarge', 'db.t2.medium', 'db.m2.4xlarge', 'db.r3.8xlarge', 'db.r4.2xlarge', 'db.m2.4xlarge', 'db.t2.xlarge',
     'db.r4.large', 'db.m4.large', 'db.r3.large', 'db.t2.large', 'db.r3.8xlarge', 'db.r3.2xlarge', 'db.r4.16xlarge',
     'db.m4.xlarge', 'db.r3.4xlarge', 'db.m4.10xlarge', 'db.m1.small', 'db.t2.large', 'db.m4.16xlarge', 'db.m4.large',
     'db.r3.2xlarge', 'db.t2.xlarge', 'db.t1.micro', 'db.m1.small', 'db.r3.8xlarge', 'db.r3.large', 'db.m1.medium',
     'db.m4.4xlarge', 'db.t2.medium', 'db.t2.micro', 'db.r3.large', 'db.m1.large', 'db.r4.8xlarge', 'db.m1.small',
     'db.m4.xlarge', 'db.m1.medium', 'db.t2.medium', 'db.m3.medium', 'db.r3.2xlarge', 'db.t2.large', 'db.m4.4xlarge',
     'db.m4.2xlarge', 'db.t2.small', 'db.m3.xlarge', 'db.t2.micro', 'db.r4.large', 'db.m3.xlarge', 'db.m2.xlarge',
     'db.t2.micro', 'db.m3.large', 'db.m2.xlarge', 'db.m4.4xlarge', 'db.m4.16xlarge', 'db.t1.micro', 'db.m4.4xlarge',
     'db.r4.2xlarge', 'db.m1.small', 'db.r4.2xlarge', 'db.m3.large', 'db.t2.2xlarge', 'db.r3.large', 'db.t2.micro',
     'db.r4.large', 'db.r3.2xlarge', 'db.m3.xlarge', 'db.m2.2xlarge', 'db.r4.16xlarge', 'db.m3.large', 'db.r3.4xlarge',
     'db.m3.2xlarge', 'db.t1.micro', 'db.m2.2xlarge', 'db.m3.large', 'db.r4.16xlarge', 'db.r4.large', 'db.t2.small',
     'db.m3.2xlarge', 'db.t2.small', 'db.r4.4xlarge', 'db.r3.8xlarge', 'db.m2.4xlarge', 'db.t2.medium', 'db.r4.4xlarge',
     'db.r3.large', 'db.m1.xlarge', 'db.m4.xlarge', 'db.m1.xlarge', 'db.m4.xlarge', 'db.t2.medium', 'db.m1.large',
     'db.t2.micro', 'db.m1.large', 'db.m1.large', 'db.m1.large', 'db.r3.8xlarge', 'db.r4.4xlarge', 'db.r3.large',
     'db.m2.4xlarge', 'db.r3.4xlarge', 'db.m4.xlarge', 'db.r4.2xlarge', 'db.r3.8xlarge', 'db.r3.xlarge',
     'db.r3.2xlarge', 'db.m2.2xlarge', 'db.m4.large', 'db.t2.large', 'db.m3.large', 'db.t2.large', 'db.m4.xlarge',
     'db.t2.micro', 'db.r3.xlarge', 'db.t2.2xlarge', 'db.r4.16xlarge', 'db.r3.xlarge', 'db.r3.xlarge', 'db.m3.medium',
     'db.m2.4xlarge', 'db.r3.8xlarge', 'db.m3.large', 'db.m1.large', 'db.t2.xlarge', 'db.m1.large', 'db.r3.large',
     'db.r3.large', 'db.r4.16xlarge', 'db.t2.2xlarge', 'db.r4.large', 'db.m4.large', 'db.m3.large', 'db.r4.4xlarge',
     'db.r3.2xlarge', 'db.m4.large', 'db.m4.2xlarge', 'db.m1.medium', 'db.m4.10xlarge', 'db.r4.16xlarge',
     'db.m3.xlarge', 'db.m4.xlarge', 'db.r3.4xlarge', 'db.r3.4xlarge', 'db.m2.xlarge', 'db.m4.16xlarge',
     'db.m4.2xlarge', 'db.m2.xlarge', 'db.m4.4xlarge', 'db.r3.8xlarge', 'db.m3.2xlarge', 'db.m4.4xlarge',
     'db.r3.4xlarge', 'db.r4.2xlarge', 'db.t2.medium', 'db.m3.2xlarge', 'db.m3.xlarge', 'db.m3.medium', 'db.m2.xlarge',
     'db.r4.large', 'db.r4.4xlarge', 'db.t2.small', 'db.r3.4xlarge', 'db.r4.2xlarge', 'db.r4.4xlarge', 'db.m1.medium',
     'db.m3.2xlarge', 'db.t2.2xlarge', 'db.m4.2xlarge', 'db.m4.xlarge', 'db.m4.4xlarge', 'db.r3.xlarge', 'db.r4.xlarge',
     'db.r4.2xlarge', 'db.r3.8xlarge', 'db.m1.small', 'db.r3.4xlarge', 'db.m3.medium', 'db.r3.xlarge', 'db.m3.medium',
     'db.r3.large', 'db.t2.small', 'db.m1.small', 'db.m4.10xlarge', 'db.m4.xlarge', 'db.m1.xlarge', 'db.m2.xlarge',
     'db.r3.xlarge', 'db.t2.micro', 'db.r3.4xlarge', 'db.r3.4xlarge', 'db.m4.2xlarge', 'db.m4.large', 'db.m4.xlarge',
     'db.m4.10xlarge', 'db.m1.small', 'db.r3.large', 'db.m1.xlarge', 'db.t2.2xlarge', 'db.m2.4xlarge', 'db.m2.2xlarge',
     'db.t2.micro', 'db.r3.2xlarge', 'db.r4.2xlarge', 'db.m4.large', 'db.r4.xlarge', 'db.r4.8xlarge', 'db.r3.large',
     'db.t2.medium', 'db.m2.4xlarge', 'db.m1.small', 'db.m4.2xlarge', 'db.m2.2xlarge', 'db.t2.small', 'db.r4.4xlarge',
     'db.m4.xlarge', 'db.r4.8xlarge', 'db.m1.medium', 'db.r4.16xlarge', 'db.m3.medium', 'db.t2.xlarge', 'db.r3.large',
     'db.m2.2xlarge', 'db.t2.2xlarge', 'db.r3.8xlarge', 'db.m3.large', 'db.t2.2xlarge', 'db.m3.xlarge',
     'db.m4.10xlarge', 'db.m1.xlarge', 'db.t1.micro', 'db.t2.micro', 'db.m4.2xlarge', 'db.r3.large', 'db.m4.10xlarge',
     'db.r4.large', 'db.m3.xlarge', 'db.t1.micro', 'db.r4.2xlarge', 'db.m4.2xlarge', 'db.r4.2xlarge', 'db.m2.4xlarge',
     'db.m3.large', 'db.r4.4xlarge', 'db.m3.2xlarge', 'db.m2.xlarge', 'db.m1.medium', 'db.r3.large', 'db.m4.2xlarge',
     'db.m1.medium', 'db.m3.xlarge', 'db.r3.4xlarge', 'db.t2.2xlarge', 'db.m3.xlarge', 'db.r4.xlarge', 'db.r3.2xlarge',
     'db.t2.large', 'db.m3.xlarge', 'db.m4.xlarge', 'db.r4.2xlarge', 'db.m2.xlarge', 'db.r4.xlarge', 'db.m4.xlarge',
     'db.m3.large', 'db.r3.8xlarge', 'db.r3.4xlarge', 'db.m4.xlarge', 'db.r4.4xlarge', 'db.r4.large', 'db.t2.small',
     'db.r4.16xlarge', 'db.m4.10xlarge', 'db.m3.medium', 'db.m2.2xlarge', 'db.m1.small', 'db.m3.xlarge', 'db.t2.medium',
     'db.r4.4xlarge', 'db.m3.2xlarge', 'db.m2.xlarge', 'db.r4.large', 'db.t2.small', 'db.t1.micro', 'db.t2.micro',
     'db.m4.xlarge', 'db.r3.2xlarge', 'db.r4.2xlarge', 'db.t2.medium', 'db.r4.16xlarge', 'db.m4.large', 'db.m3.medium',
     'db.r3.xlarge', 'db.r3.xlarge', 'db.m1.medium', 'db.m1.medium', 'db.m4.10xlarge', 'db.r4.4xlarge', 'db.m3.medium',
     'db.r4.4xlarge', 'db.m2.2xlarge', 'db.m4.4xlarge', 'db.r4.16xlarge', 'db.m1.small', 'db.t1.micro', 'db.r3.2xlarge',
     'db.m2.2xlarge', 'db.t2.small', 'db.m1.large', 'db.m2.xlarge', 'db.m2.4xlarge', 'db.m3.medium', 'db.t1.micro',
     'db.m1.small', 'db.r4.large', 'db.t2.large', 'db.m4.10xlarge', 'db.r4.8xlarge', 'db.r4.16xlarge', 'db.m3.2xlarge',
     'db.r3.8xlarge', 'db.t2.xlarge', 'db.m1.xlarge', 'db.m4.4xlarge', 'db.m1.small', 'db.r3.xlarge', 'db.m4.4xlarge',
     'db.m4.2xlarge', 'db.m3.large', 'db.m4.2xlarge', 'db.m2.2xlarge', 'db.m3.medium', 'db.m1.xlarge', 'db.r4.large',
     'db.m2.2xlarge', 'db.r3.xlarge', 'db.m4.10xlarge', 'db.m3.2xlarge', 'db.m4.2xlarge', 'db.t2.small', 'db.r3.xlarge',
     'db.m1.large', 'db.r3.xlarge', 'db.r4.2xlarge', 'db.m1.xlarge', 'db.r4.8xlarge', 'db.t2.large', 'db.m4.16xlarge',
     'db.m4.xlarge', 'db.m4.2xlarge', 'db.m4.large', 'db.r4.2xlarge', 'db.m2.2xlarge', 'db.m3.xlarge', 'db.m1.small',
     'db.m4.large', 'db.r4.8xlarge', 'db.r3.xlarge', 'db.m4.xlarge', 'db.r4.4xlarge', 'db.m3.xlarge', 'db.m1.xlarge',
     'db.m2.4xlarge']

    rds_comp_set=set(rds_comp_list)
    rds_comp_eng=set()

    #Initialize List of Available Compute Engines
    for rds_type in sorted(rds_comp_set):
        rds_comp_eng.add(".".join([rds_type.split(".")[0], rds_type.split(".")[1]]))

    print("Available RDS Compute Engine Class - ")
    rds_eng_list=list(sorted(rds_comp_eng))

    for i in rds_eng_list:
        print("%d) %s " %(rds_eng_list.index(i),i))
    rds_eng_dict=switch(rds_eng_list,rds_comp_list)
    rds_eng_user_input = input("Enter the RDS Engine Serial(0,1,6 is not option): ")
    rds_restrict=[0,1,6]
    if int(rds_eng_user_input) in rds_restrict:
        print("Engine selected does not support Encryption")
        return 1

    rds_comp_user_list=rds_eng_dict[rds_eng_list[int(rds_eng_user_input)]]
    print("Available RDS Compute Engines - ")
    for i in rds_comp_user_list:
        print("%d) %s " %(rds_comp_user_list.index(i),i))
    rds_comp_user_input = input("Enter the RDS Compute Serial : ")
    v_rdscom=rds_comp_user_list[int(rds_comp_user_input)]

    print("Selected RDBMS Engine - %s " %v_rdbms)
    print("Selected Compute Class - %s " %v_rdscom)
    acct_type=input("Enter AWS A/C Type (preprod/prd):")
    env=input("Enter Environment(qal/e2e/dev/prf/pds/prd) : ")
    app=input("Enter 3 Letters of App : ")
    prefix="-".join([env,app,acct_type])
    print(prefix)
    rdscomplist=[v_rdbms,v_rdscom,prefix,v_engver]
    return rdscomplist




def switch(eng_list,comp_list):
    eng_set=set(eng_list)
    comp_set=set(comp_list)
    eng_list=list(sorted(eng_set))
    comp_list=list(sorted(comp_set))
    #print(comp_list)
    #print(eng_list)
    #Create Compute Dictionary
    rds_com_dict={}
    for eng in eng_list:
        rds_eng_lst=[]
        for comp in comp_list:
            if ".".join([comp.split(".")[0], comp.split(".")[1]])==eng:
                rds_eng_lst.append(comp)
        #print(rds_eng_lst)
        rds_com_dict[eng]=rds_eng_lst
    return rds_com_dict





def get_input(rds_lst):
    v_rds=boto3.client('rds')
    v_dbname = input("Enter the Database Name : ")
    rds_lst.append(v_dbname)
    v_dbinstance = input("Enter the Database Instance Identifier : ")
    rds_lst.append(v_dbinstance)
    v_stglist=[('Standard','standard'),('General SSD','gp2'),('Provisioned SSD','io1')]
    print("Available the Storage Type - ")
    for i in range(0,len(v_stglist)):
        print("%d) %s" % (i, v_stglist[i][0]))
    v_input=input("Enter the Storage Type : ")
    v_stgtype=v_stglist[int(v_input)][1]
    rds_lst.append(v_stgtype)

    v_allocatedstorage=int(input("Enter the Amount of Storage required in GB : "))

    if v_stgtype == 'io1' and v_allocatedstorage < 100:
        v_allocatedstorage=100
    if v_allocatedstorage < 20:
        v_allocatedstorage=20
    print("Adjusted Allocated Storage for Storage type : %d " %v_allocatedstorage)
    rds_lst.append(v_allocatedstorage)

    v_musername=input("Enter the Master username : ")
    rds_lst.append(v_musername)
    v_mpassword=input("Enter the Master Password (Atleast 8 characters): ")
    rds_lst.append(v_mpassword)

    v_input=input("Multi AZ RDS Deployment (Y/N) : ")

    v_multiazdict={'Y':True,'N':False}
    v_multiaz=v_multiazdict[v_input]

    rds_lst.append(v_multiaz)

    v_maintwindow='Sun:01:00-Sun:01:30'
    print("Preferred Maintenance Window selected %s (UTC). Change it later if needed." %v_maintwindow)
    rds_lst.append(v_maintwindow)

    v_backupretention=7
    print("Backup retention taken as %d Days. Change it later if needed." %v_backupretention)
    rds_lst.append(v_backupretention)

    v_backupwindow='00:00-00:30'
    print("Preferred Backup Window selected %s (UTC). Change it later if needed." %v_backupwindow)
    rds_lst.append(v_backupwindow)

    v_portdefault = {'mysql': 3306, 'aurora': 3306, 'oracle-ee': 1521, 'sqlserver-ee': 1433}
    print("Default ports : %s " %v_portdefault)
    v_port=input("Enter the RDS Port for App connections (Press Enter for Default): ")

    if v_port == "":
        v_port=v_portdefault[rds_lst[0]]
    rds_lst.append(int(v_port))

    print("Enter the serial# of Listed Engine version : ")
    response = v_rds.describe_db_engine_versions(
        DefaultOnly=False,
        Engine=rds_lst[0],
        EngineVersion=rds_lst[3],
        ListSupportedCharacterSets=True,
    )

    for i in range(0, len(response['DBEngineVersions'])):
        print(" %d) %s" % (i, response['DBEngineVersions'][i]['EngineVersion']))

    v_input = input("Enter the serial # : ")
    v_rdbms_version = response['DBEngineVersions'][int(v_input)]['EngineVersion']
    rds_lst.append(v_rdbms_version)
    print(v_rdbms_version)

    if rds_lst[0]=="oracle-ee":
        for i in response['DBEngineVersions'][int(v_input)]['SupportedCharacterSets']:
            print("%d ) %s" % (
            response['DBEngineVersions'][int(v_input)]['SupportedCharacterSets'].index(i), i['CharacterSetName']))

        v_character = \
        response['DBEngineVersions'][int(v_input)]['SupportedCharacterSets'][int(input("Enter the Serial # : "))][
            'CharacterSetName']

        rds_lst.append(v_character)
    else:
        rds_lst.append('')

    v_autominorupgrade=False
    rds_lst.append(v_autominorupgrade)

    v_license_lst={'mysql':'general-public-license','oracle-ee':'bring-your-own-license'}
    v_license=v_license_lst[rds_lst[0]]
    rds_lst.append(v_license)

    v_iops=1000
    rds_lst.append(v_iops)

    v_public=False
    rds_lst.append(v_public)

    v_tags=[{'Key':'Name','Value':v_dbname}]
    rds_lst.append(v_tags)

    v_stg_encrypt=True
    rds_lst.append(v_stg_encrypt)

    v_kmsid=create_kmsarn()
    rds_lst.append(v_kmsid)

    v_copytags=True
    rds_lst.append(v_copytags)

    print(rds_lst)
    return rds_lst


def create_rds(rds_lst):
    v_rds = boto3.client('rds')
    rds_dict = {'DBName': rds_lst[8],
                'DBInstanceIdentifier': rds_lst[9],
                'AllocatedStorage': rds_lst[11],
                'DBInstanceClass': rds_lst[1],
                'Engine': rds_lst[0],
                'MasterUsername': rds_lst[12],
                'MasterUserPassword': rds_lst[13],
                'VpcSecurityGroupIds': [rds_lst[5]],
                'DBSubnetGroupName': rds_lst[4],
                'PreferredMaintenanceWindow': rds_lst[15],
                'DBParameterGroupName': rds_lst[7],
                'BackupRetentionPeriod': rds_lst[16],
                'PreferredBackupWindow': rds_lst[17],
                'Port': rds_lst[18],
                'MultiAZ': rds_lst[14],
                'EngineVersion': rds_lst[19],
                'AutoMinorVersionUpgrade': rds_lst[21],
                'LicenseModel': rds_lst[22],
                'Iops': rds_lst[23],
                'OptionGroupName': rds_lst[6],
                'CharacterSetName': rds_lst[20],
                'PubliclyAccessible': rds_lst[24],
                'Tags': rds_lst[25],
                'StorageType': rds_lst[10],
                'StorageEncrypted': rds_lst[26],
                'KmsKeyId': rds_lst[27],
                'CopyTagsToSnapshot': rds_lst[28]}

    if rds_dict['Engine'] == 'mysql' and rds_dict['StorageType'] == 'gp2':
        response = v_rds.create_db_instance(
            DBName=rds_lst[8],
            DBInstanceIdentifier=rds_lst[9],
            AllocatedStorage=rds_lst[11],
            DBInstanceClass=rds_lst[1],
            Engine=rds_lst[0],
            MasterUsername=rds_lst[12],
            MasterUserPassword=rds_lst[13],
            VpcSecurityGroupIds=[rds_lst[5]],
            DBSubnetGroupName=rds_lst[4],
            PreferredMaintenanceWindow=rds_lst[15],
            DBParameterGroupName=rds_lst[7],
            BackupRetentionPeriod=rds_lst[16],
            PreferredBackupWindow=rds_lst[17],
            Port=rds_lst[18],
            MultiAZ=rds_lst[14],
            EngineVersion=rds_lst[19],
            AutoMinorVersionUpgrade=rds_lst[21],
            LicenseModel=rds_lst[22],
            OptionGroupName=rds_lst[6],
            PubliclyAccessible=rds_lst[24],
            Tags=rds_lst[25],
            StorageType=rds_lst[10],
            StorageEncrypted=rds_lst[26],
            KmsKeyId=rds_lst[27],
            CopyTagsToSnapshot=rds_lst[28]
        )
        print(response)
    elif rds_dict['Engine'] == 'mysql' and rds_dict['StorageType'] == 'io1':
        response = v_rds.create_db_instance(
            DBName=rds_lst[8],
            DBInstanceIdentifier=rds_lst[9],
            AllocatedStorage=rds_lst[11],
            DBInstanceClass=rds_lst[1],
            Engine=rds_lst[0],
            MasterUsername=rds_lst[12],
            MasterUserPassword=rds_lst[13],
            VpcSecurityGroupIds=[rds_lst[5]],
            DBSubnetGroupName=rds_lst[4],
            PreferredMaintenanceWindow=rds_lst[15],
            DBParameterGroupName=rds_lst[7],
            BackupRetentionPeriod=rds_lst[16],
            PreferredBackupWindow=rds_lst[17],
            Port=rds_lst[18],
            MultiAZ=rds_lst[14],
            EngineVersion=rds_lst[19],
            AutoMinorVersionUpgrade=rds_lst[21],
            LicenseModel=rds_lst[22],
            Iops=rds_lst[23],
            OptionGroupName=rds_lst[6],
            PubliclyAccessible=rds_lst[24],
            Tags=rds_lst[25],
            StorageType=rds_lst[10],
            StorageEncrypted=rds_lst[26],
            KmsKeyId=rds_lst[27],
            CopyTagsToSnapshot=rds_lst[28]
        )
        print(response)
    elif rds_dict['Engine'] == 'oracle-ee' and rds_dict['StorageType'] == 'gp2':
        response = v_rds.create_db_instance(
            DBName=rds_lst[8],
            DBInstanceIdentifier=rds_lst[9],
            AllocatedStorage=rds_lst[11],
            DBInstanceClass=rds_lst[1],
            Engine=rds_lst[0],
            MasterUsername=rds_lst[12],
            MasterUserPassword=rds_lst[13],
            VpcSecurityGroupIds=[rds_lst[5]],
            DBSubnetGroupName=rds_lst[4],
            PreferredMaintenanceWindow=rds_lst[15],
            DBParameterGroupName=rds_lst[7],
            BackupRetentionPeriod=rds_lst[16],
            PreferredBackupWindow=rds_lst[17],
            Port=rds_lst[18],
            MultiAZ=rds_lst[14],
            EngineVersion=rds_lst[19],
            AutoMinorVersionUpgrade=rds_lst[21],
            LicenseModel=rds_lst[22],
            OptionGroupName=rds_lst[6],
            CharacterSetName=rds_lst[20],
            PubliclyAccessible=rds_lst[24],
            Tags=rds_lst[25],
            StorageType=rds_lst[10],
            StorageEncrypted=rds_lst[26],
            KmsKeyId=rds_lst[27],
            CopyTagsToSnapshot=rds_lst[28]
        )
        print(response)
    elif rds_dict['Engine'] == 'oracle-ee' and rds_dict['StorageType'] == 'io1':
        response = v_rds.create_db_instance(
            DBName=rds_lst[8],
            DBInstanceIdentifier=rds_lst[9],
            AllocatedStorage=rds_lst[11],
            DBInstanceClass=rds_lst[1],
            Engine=rds_lst[0],
            MasterUsername=rds_lst[12],
            MasterUserPassword=rds_lst[13],
            VpcSecurityGroupIds=[rds_lst[5]],
            DBSubnetGroupName=rds_lst[4],
            PreferredMaintenanceWindow=rds_lst[15],
            DBParameterGroupName=rds_lst[7],
            BackupRetentionPeriod=rds_lst[16],
            PreferredBackupWindow=rds_lst[17],
            Port=rds_lst[18],
            MultiAZ=rds_lst[14],
            EngineVersion=rds_lst[19],
            AutoMinorVersionUpgrade=rds_lst[21],
            LicenseModel=rds_lst[22],
            Iops=rds_lst[23],
            OptionGroupName=rds_lst[6],
            CharacterSetName=rds_lst[20],
            PubliclyAccessible=rds_lst[24],
            Tags=rds_lst[25],
            StorageType=rds_lst[10],
            StorageEncrypted=rds_lst[26],
            KmsKeyId=rds_lst[27],
            CopyTagsToSnapshot=rds_lst[28]
        )
        print(response)



def create_subnetgrp(subnet_list,prefix):
    v_rds=boto3.client('rds')
    prefix="-".join([prefix,"sub-grp"])
    env=prefix.split("-",1)[0]
    desc=" ".join([env,"RDS DB subnet group"])
    try:
        v_sub_dict=v_rds.create_db_subnet_group(DBSubnetGroupDescription=desc,DBSubnetGroupName=prefix,SubnetIds=subnet_list)
        print(v_sub_dict['DBSubnetGroup']['DBSubnetGroupName'])
        return v_sub_dict['DBSubnetGroup']['DBSubnetGroupName']
    except:
        print(prefix)
        return prefix

def create_securitygrp(prefix,vpc):
    v_ec2=boto3.client('ec2')
    prefix="-".join([prefix,"sec-grp"])
    env=prefix.split("-",1)[0]
    desc=" ".join([env,"RDS DB Security group"])
    try:
        v_sec_dict=v_ec2.create_security_group(Description=desc,GroupName=prefix,VpcId=vpc)
        response=v_ec2.create_tags(Resources=[v_sec_dict['GroupId']],Tags=[{'Key':'Name','Value':prefix}])
        print(v_sec_dict['GroupId'])
        return v_sec_dict['GroupId']
    except:
        response = v_ec2.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [prefix]}])
        prefix=response['SecurityGroups'][0]['GroupId']
        print(prefix)
        return prefix


def create_optiongrp(dbeng,version,prefix):
    v_rds = boto3.client('rds')
    prefix = "-".join([prefix, "opt-grp"])
    env = prefix.split("-", 1)[0]
    desc=" ".join([env,"RDS ",dbeng,version," DB OPT Group"])
    try:

        response=v_rds.create_option_group(
            EngineName=dbeng,
            MajorEngineVersion=version,
            OptionGroupDescription=desc,
            OptionGroupName=prefix
        )
        print(response['OptionGroup']['OptionGroupName'])
        return response['OptionGroup']['OptionGroupName']
    except:
        print(prefix)
        return prefix


def create_paramgrp(dbeng,version,prefix):
    v_rds = boto3.client('rds')
    prefix = "-".join([prefix, "prm-grp"])
    env = prefix.split("-", 1)[0]
    desc=" ".join([env,"RDS ",dbeng,version," DB PRM Group"])
    v_dbparam=v_rds.describe_db_engine_versions()
    v_len = len(v_dbparam['DBEngineVersions'])
    v_prm=set()
    for i in range(0,v_len):
        if dbeng == v_dbparam['DBEngineVersions'][i]['Engine'] and version in v_dbparam['DBEngineVersions'][i][
            'DBParameterGroupFamily']:
            v_prm.add(v_dbparam['DBEngineVersions'][i]['DBParameterGroupFamily'])
    print(v_prm)
    try:
        response=v_rds.create_db_parameter_group(DBParameterGroupFamily=v_prm.pop(),DBParameterGroupName=prefix,Description=desc)
        print(response['DBParameterGroup']['DBParameterGroupName'])
        return response['DBParameterGroup']['DBParameterGroupName']
    except:
        print(prefix)
        return prefix

def create_kmsarn():
    client = boto3.client('kms')
    response = client.create_key(
        Description='Encryption Key for RDS',
        KeyUsage='ENCRYPT_DECRYPT',
        Origin='AWS_KMS',
        BypassPolicyLockoutSafetyCheck=False,
        Tags=[
            {
                'TagKey': 'Name',
                'TagValue': 'RDS_Key'
            },
        ]
    )
    v_kmsarn = response['KeyMetadata']['Arn']
    prefix="".join(["alias/RDS-",rds_lst[2],''.join(random.choice('0123456789ABCDEF') for i in range(16))])
    response = client.create_alias(AliasName=prefix,TargetKeyId=v_kmsarn)
    response = client.enable_key_rotation(KeyId=v_kmsarn)
    return v_kmsarn



v_vpcid=get_vpcid()
print(v_vpcid)
rdssubnetlist=get_subnet(v_vpcid)
print (v_vpcid)
print(rdssubnetlist)
rdscomplist=get_rdsinput()
if rdscomplist == 1:
    exit(1)
print(rdscomplist)
sub_grp=create_subnetgrp(rdssubnetlist,rdscomplist[2])
sec_grp=create_securitygrp(rdscomplist[2],v_vpcid)
opt_grp=create_optiongrp(rdscomplist[0],rdscomplist[3],rdscomplist[2])
param_grp=create_paramgrp(rdscomplist[0],rdscomplist[3],rdscomplist[2])
rds_lst=rdscomplist+[sub_grp,sec_grp,opt_grp,param_grp]
print(rds_lst)
aws_rds_lst=get_input(rds_lst)
response=create_rds(aws_rds_lst)
print(response)


