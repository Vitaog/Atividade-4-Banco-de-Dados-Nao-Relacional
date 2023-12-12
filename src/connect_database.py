from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

def conectar_cassandra():
    cloud_config = {
        'secure_connect_bundle': 'src/secure-connect-mercado-livre.zip'
    }

    with open("src/vitor.oliveira67@fatec.sp.gov.br-token.json") as f:
        secrets = json.load(f)

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    
    session = cluster.connect(keyspace='mercado_livre_cassandra')

    return session
