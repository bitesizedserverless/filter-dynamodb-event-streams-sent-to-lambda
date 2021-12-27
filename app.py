#!/usr/bin/env python3
"""The main app. Contains all the stacks."""

# Standard library imports
# -

# Related third party imports
# -

# Local application/library specific imports
from aws_cdk import core as cdk
from config import Config
from filter_dynamodb_event_streams_sent_to_lambda.filter_dynamodb_event_streams_sent_to_lambda_stack import (
    FilterDynamodbEventStreamsSentToLambdaStack,
)

config = Config()

app = cdk.App()
FilterDynamodbEventStreamsSentToLambdaStack(
    scope=app,
    construct_id="FilterDynamodbEventStreamsSentToLambdaStack",
    config=config.base(),
)

app.synth()
