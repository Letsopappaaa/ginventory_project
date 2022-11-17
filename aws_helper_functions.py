
import json
import time
import pandas as pd

def create_IAM_role_Redshift_to_S3(iam, ROLE_NAME):
    '''
    Create IAM role so we can access S3 from Redshift
    Returns roleArn
    '''
    try:
        print("Creating a new IAM Role") 
        dwhRole = iam.create_role(
            Path='/',
            RoleName=ROLE_NAME,
            Description = "Allows Redshift clusters to call AWS services on your behalf.",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                'Effect': 'Allow',
                'Principal': {'Service': 'redshift.amazonaws.com'}}],
                'Version': '2012-10-17'})
        )    
    except Exception as e:
        print(e)

    # Attach S3 access policy to our new role

    iam.attach_role_policy(RoleName=ROLE_NAME,
                        PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                        )['ResponseMetadata']['HTTPStatusCode']

    print("Get the IAM role ARN")
    roleArn = iam.get_role(RoleName=ROLE_NAME)['Role']['Arn']
    
    print(roleArn)
    return roleArn



def create_redshift_cluster(redshift_client, CLUSTER_ID, CLUSTER_TYPE, NODE_TYPE, NUMBER_OF_NODES, DB_NAME, DB_USER, DB_PASSWORD, roleArn):

    # Create redshift cluster
    try:
        response = redshift_client.create_cluster(
            ClusterType= CLUSTER_TYPE,
            NodeType=NODE_TYPE,
            NumberOfNodes=int(NUMBER_OF_NODES),

            #Identifiers & Credentials
            DBName=DB_NAME,
            ClusterIdentifier=CLUSTER_ID,
            MasterUsername=DB_USER,
            MasterUserPassword=DB_PASSWORD,
            
            #Roles (for s3 access)
            IamRoles=[roleArn]  
        )

        print(f"Creating new cluster: {CLUSTER_ID}")

        # Wait for the new cluster status change to available
        create_waiter = redshift_client.get_waiter("cluster_available")
        create_waiter.wait(
                ClusterIdentifier = CLUSTER_ID,
                WaiterConfig = {
                    "Delay": 10,
                    "MaxAttempts": 30
                }
            )

        print("New cluster named '{}' created and available".format(CLUSTER_ID))

    except Exception as e:
        if 'ClusterAlreadyExists' in str(e):
            print(f'Cluster with the same name({CLUSTER_ID}) already exists.')
        else:
            print(e)

    myClusterProps = redshift_client.describe_clusters(ClusterIdentifier=CLUSTER_ID)['Clusters'][0]
    prettyRedshiftProps(myClusterProps)


# Prettify redshift cluster properties
def prettyRedshiftProps(props):
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])



# Set a VPC security group rule to authorize ingress to the cluster's VPC Security Group
# Extract cluster info
def set_vpc_security_group(redshift_client, CLUSTER_ID, ec2):
    vpc_security_group_id = redshift_client.describe_clusters(ClusterIdentifier=CLUSTER_ID)['Clusters'][0]["VpcSecurityGroups"][0]["VpcSecurityGroupId"]
    print(f'VPC security group ID: {vpc_security_group_id}')
    try:
        # Extract security group for the VPC
        vpc_sg = ec2.SecurityGroup(id = vpc_security_group_id)
        
        # Authorize connection to the VPC
        vpc_sg.authorize_ingress(
            GroupName = vpc_sg.group_name,
            CidrIp = "0.0.0.0/0",
            IpProtocol = "TCP",
            FromPort = 5439,
            ToPort = 5439
        )
        print("Ingress to the VPC authorized")
        
    except Exception as e:
        
        # Check if the error is a duplication error
        if "InvalidPermission.Duplicate" in str(e):
            print("Rule requested already exists")
        else:
            print(e)



# Function to return pandas df from redshift response Id

def redshift_get_statement_result_to_dataframe(redshift_data, response_id):
    '''
    Returns pandas dataframe of the statement Id passed from the response object 
    of the redshift-data.execute_statement method. If statement has no result set
    a message is returned.
    response = redshift_data.execute_statement(...)
    response_id = response['Id]
    '''
    # Timeout after 30 seconds of no FAILED or FINISHED status response
    timeout = time.time() + 30

    while time.time() < timeout:
        describe_obj = redshift_data.describe_statement(Id=response_id)
        status = describe_obj['Status']
        if status == 'FINISHED':
            if describe_obj['HasResultSet'] == True:
                statement_result = redshift_data.get_statement_result(Id=response_id)
                try:
                    if len(statement_result['Records']) == 0:
                        return 'Result set contains 0 rows.'
                    df = pd.DataFrame(statement_result['Records'])
                    df.rename(columns=pd.DataFrame(statement_result['ColumnMetadata']).name, inplace=True)
                    df = df.apply(pd.Series)

                    for column in df.columns:
                        df[column] = df[column].apply(pd.Series)
                    return df
                except Exception as e:
                    raise ValueError('Query status: ' + status + '\n' + describe_obj['Error'])
            else:
                return 'Statement has no result set. Call with sql statement that produces a result set.'
        elif status == 'FAILED':
            raise ValueError('Query status: ' + status + '\n' + describe_obj['Error'])
        else:
            time.sleep(1)
    else:
        raise TimeoutError('Timeout limit exceeded.')
