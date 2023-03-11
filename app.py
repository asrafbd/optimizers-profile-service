from flask import Flask,jsonify,request
import psycopg2
import boto3
import os

app = Flask(__name__)

# set up connection to PostgreSQL database
database_name = os.getenv('DATABASE_NAME')
database_user = os.getenv('DATABASE_USER')
database_password = os.getenv('DATABASE_PASSWORD')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')

# conn = psycopg2.connect(
#     database=database_name,
#     user=database_user,
#     password=database_password,
#     host=database_host,
#     port=database_port
# )

def connect_to_s3_client():
    """connect to s3 client"""
    try:
        service = 's3'
        access_key = "VZZOCH9RS378DIYM5WC8"
        secret_access_key = "p1cyqBjGto5aZzfk07Ck8ScqtRPUsBIBHOVoomwQ"
        s3_client = boto3.client(service_name=service, endpoint_url="https://s3.brilliant.com.bd",
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_access_key)

        print("connected to aws s3 service")
        return s3_client
    except Exception as ex:
        print("error occurs while connecting to s3 service: %s", ex)

def get_presigned_url(image_location):
    try:
        s3_client = connect_to_s3_client()

        if image_location:
            url = image_location
            return s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': 'profile-bucket', 'Key': url},
                ExpiresIn=3600
            )
    except Exception as ex:
        print("error occurs while downloading file from s3: %s", ex)

@app.route('/')
def hello_world():
    return 'Hello world'


# Need to refactor the route
@app.route('/reverser', methods=['POST'])
def get_user_contact():
    data = request.json
    num = data.get('num')
    conn = psycopg2.connect(
        database=database_name,
        user=database_user,
        password=database_password,
        host=database_host,
        port=database_port
    )
    cur = conn.cursor()
    cur.execute("select a.name,b.pic from users as a join user_data as b on a.number=b.phone where a.number=%s", (num,))
    row = cur.fetchone()

    if row is None:
        return jsonify({'num': 'User not found'})
    else:
        url = get_presigned_url('images/'+num+'.jpg')
        return jsonify({'num': row[0]['name'], 'pic_url': url})

if __name__ == "__main__":
     app.run()