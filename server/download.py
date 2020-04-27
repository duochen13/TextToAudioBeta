from google.cloud import storage


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    # storage_client = storage.Client("texttovoice-275117")
    storage_client = storage.Client.from_service_account_json("/Users/duochen/Desktop/Winter20/TextToAudioBeta/server/keyFile.json")

    bucket = storage_client.get_bucket(bucket_name)
    
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

download_blob("text_audio_image_bucekt", "test_img.png", "test_img.png")
