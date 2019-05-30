[![Build Status](https://travis-ci.org/usdot-jpo-sdc-projects/sdc-dot-waze-poll-for-batches-to-process.svg?branch=master)](https://travis-ci.org/usdot-jpo-sdc-projects/sdc-dot-waze-poll-for-batches-to-process)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc-projects_sdc-dot-waze-poll-for-batches-to-manifest&metric=coverage)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc-projects_sdc-dot-waze-poll-for-batches-to-manifest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc-projects_sdc-dot-waze-poll-for-batches-to-manifest&metric=alert_status)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc-projects_sdc-dot-waze-poll-for-batches-to-manifest)
# sdc-dot-waze-poll-for-batches-to-process
Lambda function that polls for new batches for data to be persisted into Redshift. Reads the message from queue and sends a notification to SNS topic
