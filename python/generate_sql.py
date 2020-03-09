import yaml
from jinja2 import Template
from google.cloud import bigquery
import logging
import argparse

import os


client =  bigquery.Client.from_service_account_json('/secrets/service-account.json')

class Field:

    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type

    def __eq__(self,other):
        return (self.name == other.name) and (self.field_type == other.field_type)

    def __hash__(self):
        return hash(self.name + self.field_type)

def flatten(list_of_lists):
    return set([val for sublist in list_of_lists for val in sublist])

def test_extract_schema(client, project, dataset_id, table_id):

    dataset_ref = client.dataset(dataset_id, project=project)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)  # API Request

    # View table properties
    return table.schema

def get_context_structure(context):
    context_versions = [field for field in schema if context in field.name]
    type_names = {
        "INTEGER": "INT64",
        "STRING": "STRING",
        "BOOLEAN": "BOOLEAN"
    }
    context_versions_fields_superset = flatten([[Field(field.name, type_names[field.field_type])for field in version.fields] for version in context_versions])
    context_versions_fields_superset_list = context_versions_fields_superset
    context_versions_dict = [{"name": version.name, "field_names": [field.name for field in version.fields]} for version in context_versions]
    return {"name": context, "super": context_versions_fields_superset_list, "versions": context_versions_dict}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate sql to create consolidated view for events')
    parser.add_argument("--project", "-p", required=True)
    parser.add_argument("--dataset_id", "-d", required=True)
    parser.add_argument("--table_id", "-t", required=True)
    parser.add_argument("--contexts", "-c", nargs="+", required=True)
    args = parser.parse_args()
    template = open("/app/consolidated_events.sql.j2").read()
    schema = test_extract_schema(client, args.project, args.dataset_id, args.table_id)
    root_fields = [field.name for field in schema if not field.fields]
    template_config = {
        "contexts": [get_context_structure(context) for context in args.contexts], 
        "root_fields": root_fields,
        "bigquery": {
                "project": args.project,
                "dataset_id": args.dataset_id,
                "table_id": args.table_id
            }
        }
    rendered_sql = Template(template).render(template_config)
    print(rendered_sql)
