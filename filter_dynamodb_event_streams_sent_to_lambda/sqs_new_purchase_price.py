"""Module for the main SqsNewPurchasePrice Stack."""

# Standard library imports
import json

# Third party imports
from aws_cdk import core as cdk, aws_sqs as sqs, aws_lambda as lambda_

# Local application/library specific imports
from filter_dynamodb_event_streams_sent_to_lambda.lambda_function import LambdaFunction


class SqsNewPurchasePrice(cdk.Stack):
    """The SqsNewPurchasePrice Stack."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        queue: sqs.Queue,
        **kwargs,
    ) -> None:
        """
        Initialize a new SqsNewPurchasePrice Construct.

        This Construct contains the Lambda Function and Event
        Source Mapping to process events where the `event_type` is
        "NEW_PURCHASE" and the `price` is above 200.
        """
        super().__init__(scope, construct_id, **kwargs)

        # The Lambda Function to process the messages on the queue
        processor_function = LambdaFunction(
            scope=self,
            construct_id="ProcessorFunction",
            code=lambda_.Code.from_asset("lambda_functions/queue_processor"),
        )
        queue.grant_consume_messages(processor_function.function)

        new_purchase_price = lambda_.CfnEventSourceMapping(
            scope=self,
            id="NewPurchasePriceEventSourceMapping",
            function_name=processor_function.function.function_name,
            event_source_arn=queue.queue_arn,
            maximum_batching_window_in_seconds=1,
            batch_size=1,
        )

        new_purchase_price.add_property_override(
            property_path="FilterCriteria",
            value={
                "Filters": [
                    {"Pattern": json.dumps({"body": {"event_type": ["NEW_PURCHASE"]}})},
                    {
                        "Pattern": json.dumps(
                            {"body": {"price": [{"numeric": [">", 200]}]}}
                        )
                    },
                ],
            },
        )
