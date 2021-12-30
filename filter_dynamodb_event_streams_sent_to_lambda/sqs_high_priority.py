"""Module for the main SqsHighPriority Stack."""

# Standard library imports
import json

# Third party imports
from aws_cdk import core as cdk, aws_sqs as sqs, aws_lambda as lambda_

# Local application/library specific imports
from filter_dynamodb_event_streams_sent_to_lambda.lambda_function import LambdaFunction


class SqsHighPriority(cdk.Stack):
    """The SqsHighPriority Stack."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        queue: sqs.Queue,
        **kwargs,
    ) -> None:
        """
        Initialize a new SqsHighPriority Construct.

        This Construct contains the Lambda Function and Event
        Source Mapping to process events where the attribute
        "Priority" is set to the value "HIGH".
        """
        super().__init__(scope, construct_id, **kwargs)

        # The Lambda Function to process the messages on the queue
        processor_function = LambdaFunction(
            scope=self,
            construct_id="ProcessorFunction",
            code=lambda_.Code.from_asset("lambda_functions/queue_processor"),
        )
        queue.grant_consume_messages(processor_function.function)

        high_priority = lambda_.CfnEventSourceMapping(
            scope=self,
            id="HighPriorityEventSourceMapping",
            function_name=processor_function.function.function_name,
            event_source_arn=queue.queue_arn,
            maximum_batching_window_in_seconds=1,
            batch_size=1,
        )

        high_priority.add_property_override(
            property_path="FilterCriteria",
            value={
                "Filters": [
                    {
                        "Pattern": json.dumps(
                            {
                                "messageAttributes": {
                                    "Priority": {"stringValue": ["HIGH"]}
                                },
                            }
                        )
                    },
                ],
            },
        )
