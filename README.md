# snowplow-bigquery-consolidate-events

Snowplow models the raw events table in Bigquery as a wide table with all contexts (entities) added as array of structs columns. This is convenient except when you have several versions of a given context over time. Each version (minor as well as  major) is represented as a separate column, thus requiring complex self joins to read a certain context attribute over the course of time. 

Snowplow consolidated_events script offers an easy way to handle this by merging multiple versions of a context into a single array of struct column, thus preventing the need for complex self-joins.

First build the docker image by running

	make build

Then create a folder called `secrets`, with a json file called `service-account.json` with the service account json from the respective google cloud project which has access to describe the  snowplow events bigquery table

	docker run -v secrets:/secrets snowplow-bigquery-consolidate-events \
	-p project \
	-d rt_pipeline_prod1 \
	-t events \
	-c contexts_com_organisation_context_1 contexts_com_organisation_context_2


This will print the view DDL on the console.
