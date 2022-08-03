import darwin.importer as importer
from darwin.client import Client
from darwin.importer import get_importer

annotation_paths = ["<Path to annotation file to upload>"]

client = Client.local()

dataset_slug = "<dataset slug name>"

dataset = client.get_remote_dataset(dataset_slug)
parser = get_importer("darwin")
  
importer.import_annotations(dataset, parser, annotation_paths, append=False)
