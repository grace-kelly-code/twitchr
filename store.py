import firebase_admin
from firebase_admin import credentials, storage, db
import os
import dotenv
from datetime import datetime

dotenv.load_dotenv()
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ['FIREBASE_STORAGE_BUCKET'],
    'databaseURL': os.environ['FIREBASE_DATABASE_URL']
})

bucket = storage.bucket()
ref = db.reference('/')
real_time_ref = ref.child('real_time')
bird_sightings_ref = ref.child('bird_sightings')
cat_sightings_ref = ref.child('cat_sightings')
IMAGES_DIR = 'images/'


def _store_file(filename: str):
    '''Stores a file on Firebase'''
    file = os.path.basename(IMAGES_DIR + filename)
    blob = bucket.blob(file)
    outfile = IMAGES_DIR + filename
    blob.upload_from_filename(outfile)


def update_realtime(status: str, device_data: dict, filename: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file = os.path.basename(IMAGES_DIR + filename)
    data = {
        'status': status,
        'timestamp': timestamp,
        'device': device_data,
        'image': file
    }
    _store_file(filename)
    real_time_ref.push(data)


def _get_base_sighting_data(filename: str) -> dict:
    return {
        'image': os.path.basename(IMAGES_DIR + filename),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def update_bird_sightings(filename: str, bird_species: str) -> None:
    data = _get_base_sighting_data(filename)
    data['species'] = bird_species
    bird_sightings_ref.push(data)


def update_cat_sightings(filename: str) -> None:
    data = _get_base_sighting_data(filename)
    cat_sightings_ref.push(data)
