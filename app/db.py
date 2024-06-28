import json
from pathlib import Path

from cassandra.auth import PlainTextAuthProvider  # type: ignore
from cassandra.cluster import Cluster  # type: ignore
from cassandra.cqlengine import connection  # type: ignore

BASE_DIR = Path(__file__).resolve().parent

ASTRA_DB_SECURE_BUNDLE_PATH = (
    BASE_DIR / "secure-connect-video-membership-proeject.zip"
)


def get_session():

    cloud_config = {"secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH}

    with open(BASE_DIR / "video_membership_proeject-token.json") as f:
        secrets = json.load(f)

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    connection.register_connection(str(session), session=session)
    
    connection.set_default_connection(str(session))
    return session
