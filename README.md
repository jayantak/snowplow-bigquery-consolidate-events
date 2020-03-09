# snowplow-bigquery-consolidate-events

First build the docker image by running

	make build

Then create a folder called `secrets`, with a json file called `service-account.json` with the service account json from the respective google cloud project which has access to describe the  snowplow events bigquery table

	docker run -v secrets:/secrets snowplow-bigquery-consolidate-events \
	-p project \
	-d rt_pipeline_prod1 \
	-t events \
	-c contexts_com_organisation_context_1 contexts_com_organisation_context_2
