"""Module for the main DdbInsertUsers Construct."""

# Standard library imports
import json

# Third party imports
from aws_cdk import (
    core as cdk,
    aws_dynamodb as dynamodb,
    aws_sqs as sqs,
    aws_lambda as lambda_,
)

# Local application/library specific imports
from filter_dynamodb_event_streams_sent_to_lambda.lambda_function import LambdaFunction


class DdbInsertUsers(cdk.Construct):
    """The DdbInsertUsers Construct."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        table: dynamodb.Table,
        **kwargs,
    ) -> None:
        """
        Initialize a new DdbInsertUsers Construct.

        This Construct contains the Lambda Function and Event
        Source Mapping to process DynamoDB events matching newly
        inserted users.
        """
        super().__init__(scope, construct_id, **kwargs)

        # Queues to receive successes and failures when processing is complete
        failure_destination = sqs.Queue(scope=self, id="FailureQueue")

        # The Lambda Function to consume the DynamoDB Stream
        processor_function = LambdaFunction(
            scope=self,
            construct_id="ProcessorFunction",
            code=lambda_.Code.from_asset("lambda_functions/queue_processor"),
        )

        # Allow function to read the DDB Stream
        table.grant_stream_read(processor_function.function)

        # Grant the Lambda Function permissions to write to the failure destination
        failure_destination.grant_send_messages(processor_function.function)

        user_inserts_only = lambda_.CfnEventSourceMapping(
            scope=self,
            id="UserInsertsOnlyEventSourceMapping",
            function_name=processor_function.function.function_name,
            event_source_arn=table.table_stream_arn,
            maximum_batching_window_in_seconds=1,
            starting_position="TRIM_HORIZON",
            batch_size=1,
            destination_config={
                "onFailure": {
                    "destination": failure_destination.queue_arn,
                },
            },
        )

        user_inserts_only.add_property_override(
            property_path="FilterCriteria",
            value={
                "Filters": [
                    {
                        "Pattern": json.dumps(
                            {
                                "eventName": ["INSERT"],
                                "dynamodb": {
                                    "NewImage": {"EntityType": {"S": ["User"]}}
                                },
                            }
                        )
                    },
                ],
            },
        )
