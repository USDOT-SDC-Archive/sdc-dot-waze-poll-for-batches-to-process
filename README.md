
[![Build Status](https://travis-ci.com/usdot-jpo-sdc/sdc-dot-waze-poll-for-batches-to-process.svg?branch=master)](https://travis-ci.com/usdot-jpo-sdc/sdc-dot-waze-poll-for-batches-to-process)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc_sdc-dot-waze-poll-for-batches-to-process&metric=alert_status)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc_sdc-dot-waze-poll-for-batches-to-process)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc_sdc-dot-waze-poll-for-batches-to-process&metric=coverage)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc_sdc-dot-waze-poll-for-batches-to-process)
# sdc-dot-waze-poll-for-batches-to-process
This lambda function is responsible for polling the batches to start the persistence of data in Redshift.

<a name="toc"/>

## Table of Contents

[I. Release Notes](#release-notes)

[II. Overview](#overview)

[III. Design Diagram](#design-diagram)

[IV. Getting Started](#getting-started)

[V. Unit Tests](#unit-tests)

[VI. Support](#support)

---

<a name="release-notes"/>


## [I. Release Notes](ReleaseNotes.md)
TO BE UPDATED

<a name="overview"/>

## II. Overview

There are two primary functions that this lambda function serves:
* **poll_for_batches** - gets the messages from the data persistence queue to start the persistence in Redshift
* **publish_message_to_sns** - publishes the message to the SNS topic indicating that the data persistence has started for a particular batch Id.

<a name="design-diagram"/>

## III. Design Diagram

![sdc-dot-waze-poll-for-batches-to-proces](images/waze-data-persistence.png)

<a name="getting-started"/>

## IV. Getting Started

The following instructions describe the procedure to build and deploy the lambda.

### Prerequisites
* NA 

---
### ThirdParty library

*NA

### Licensed softwares

*NA

### Programming tool versions

*Python 3.6


---
### Build and Deploy the Lambda

#### Environment Variables
Below are the environment variable needed :- 

BATCH_NOTIFICATION_SNS - {arn_of_the_sns_topic_to_send_the_notification}

persistence_sqs  - {name_of_the_sqs_queue_to_poll_messages_from}

#### Build Process

**Step 1**: Setup virtual environment on your system by foloowing below link
https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python

**Step 2**: Create a script with below contents e.g(sdc-dot-waze-poll-for-batches-to-process.sh)
```#!/bin/sh

cd sdc-dot-waze-poll-for-batches-to-process
zipFileName="sdc-dot-waze-poll-for-batches-to-process.zip"

zip -r9 $zipFileName common/*
zip -r9 $zipFileName lambdas/*
zip -r9 $zipFileName README.md
zip -r9 $zipFileName poll_for_batches_to_process_handler_main.py
zip -r9 $zipFileName root.py
```

**Step 3**: Change the permission of the script file

```
chmod u+x sdc-dot-waze-poll-for-batches-to-process.sh
```

**Step 4** Run the script file
./sdc-dot-waze-poll-for-batches-to-process.sh

**Step 5**: Upload the sdc-dot-waze-poll-for-batches-to-process.zip generated from Step 4 to a lambda function via aws console.

[Back to top](#toc)

---
<a name="unit-tests"/>

## V. Unit Tests

TO BE UPDATED

---
<a name="support"/>

## VI. Support

For any queries you can reach to support@securedatacommons.com
---
[Back to top](#toc)

