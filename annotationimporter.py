import darwin.importer as importer
from darwin.client import Client
from darwin.importer import get_importer

annotation_paths = ["/Users/markcox-smith/Documents/BYOM_Examples/new_complex_json.json"]

client = Client.local()

dataset_slug = "planes"

dataset = client.get_remote_dataset(dataset_slug)
parser = get_importer("darwin")
  
importer.import_annotations(dataset, parser, annotation_paths, append=False)