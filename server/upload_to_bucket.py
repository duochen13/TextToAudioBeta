import os
from google.cloud import storage
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/duochen/Desktop/Winter20/TextToAudioBeta/server/keyFile.json"

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    # storage_client = storage.Client.from_service_account_json('keyFile.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # print(blob.public_url)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

upload_blob('text_audio_image_bucket', './resource/test_img.png', 'test_img.png')

