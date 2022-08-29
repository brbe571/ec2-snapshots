from datetime import datetime, timedelta, timezone
import sys
import boto3
import csv

# List all regions dynamically
client = boto3.client('ec2')
all_aws_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

ec2_snapshots = []
rds_snapshots = []
cache_clusters = []


def get_ec2_snapshots():
    for region in all_aws_regions:
        #get ec2 resource
        ec2 = boto3.resource('ec2', region)
        #get ec2 snapshots
        ec2_snapshots = ec2.snapshots.all()
        for snapshot in ec2_snapshots:
            return snapshot.id

# get_ec2_snapshots()

def get_rds_snapshot():
    #get rds resource
    rds = boto3.client('rds')
    global rds_snapshots
    #get rds snapshot
    rds_snapshots = rds.describe_db_snapshots()
    for snapshot in rds_snapshots['DBSnapshots']:
        return snapshot['DBSnapshotIdentifier']

# get_rds_snapshot()

def get_cache_endpoint():
    # get elasticache resource
    elasticache = boto3.client('elasticache')
    global cache_clusters
    cache_clusters = elasticache.describe_cache_clusters(ShowCacheNodeInfo=True)
    #get cache ARN endpoint
    for cluster in cache_clusters.get('CacheClusters'):
        return cluster.get('ConfigurationEndpoint')

# get_cache_endpoint()

#create csv table

# field names
fields = ['EC2', 'RDS', 'CACHE']
  
# data rows of csv file
rows = [ [get_ec2_snapshots()],
         [get_rds_snapshot()], 
         [get_cache_endpoint()]
]

# name of csv file
filename = 'snapshot.csv'
  
# writing to csv file
with open('/Users/benrobertbrowning/Desktop/Python_Projects/snapshot.csv', 'w',newline = '') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile, delimiter = ' ')
      
    # writing the fields
    csvwriter.writerow(fields)
      
    # writing the data rows
    csvwriter.writerows(rows)


 
def delete_old_snapshots(snapshot_list):
    for snapshot in snapshots:
        # get snapshot creation time
        start_time = snapshot.start_timed
        # get local time
        delete_time = datetime.now(tz=timezone.utc) - timedelta(days=365)
        # if snaspshot age is longer than 365 days
        if delete_time > start_time:
            snapshot.delete()
            



