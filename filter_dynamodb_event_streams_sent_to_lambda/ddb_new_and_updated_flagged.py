"""Module for the main DdbNewAndUpdatedFlagged Construct."""

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


class DdbNewAndUpdatedFlagged(cdk.Construct):
    """The DdbNewAndUpdatedFlagged Construct."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        table: dynamodb.Table,
        **kwargs,
    ) -> None:
        """
        Initialize a new DdbNewAndUpdatedFlagged Construct.

        This Construct contains the Lambda Function and Event
        Source Mapping to process DynamoDB events matching newly
        inserted and updated items with the `FlaggedAt` attribute set.
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

        ddb_new_and_updated_flagged = lambda_.CfnEventSourceMapping(
            scope=self,
            id="DdbNewAndUpdatedFlaggedEventSourceMapping",
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

        ddb_new_and_updated_flagged.add_property_override(
            property_path="FilterCriteria",
            value={
                "Filters": [
                    {
                        "Pattern": json.dumps(
                            {
                                "eventName": ["INSERT", "MODIFY"],
                                "dynamodb": {
                                    "NewImage": {"FlaggedAt": {"S": [{"exists": True}]}}
                                },
                            }
                        )
                    },
                    {
                        "Pattern": json.dumps(
                            {
                                "eventName": ["INSERT", "MODIFY"],
                                "dynamodb": {
                                    "NewImage": {"FlaggedAt": {"N": [{"exists": True}]}}
                                },
                            }
                        )
                    },
                ],
            },
        )
