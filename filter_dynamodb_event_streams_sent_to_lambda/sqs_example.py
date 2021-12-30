"""Module for the main SqsExample Stack."""

# Third party imports
from aws_cdk import core as cdk, aws_sqs as sqs

# Local application/library specific imports
from filter_dynamodb_event_streams_sent_to_lambda.sqs_high_priority import (
    SqsHighPriority,
)
from filter_dynamodb_event_streams_sent_to_lambda.sqs_test_prefix import (
    SqsTestPrefix,
)
from filter_dynamodb_event_streams_sent_to_lambda.sqs_new_purchase_price import (
    SqsNewPurchasePrice,
)


class SqsExample(cdk.Stack):
    """The SqsExample Stack."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        """
        Construct a new SqsExample.

        This Construct contains a source SQS Queue, a Lambda Function and
        an Event Source Mapping to connect the two.
        """
        super().__init__(scope, construct_id, **kwargs)

        # The queue that will trigger the event source mapping
        queue = sqs.Queue(scope=self, id="SourceQueue")

        # The Event Source Mapping for high priority messages
        SqsHighPriority(scope=self, construct_id="SqsHighPriority", queue=queue)
        SqsTestPrefix(scope=self, construct_id="SqsTestPrefix", queue=queue)
        SqsNewPurchasePrice(scope=self, construct_id="SqsNewPurchasePrice", queue=queue)
