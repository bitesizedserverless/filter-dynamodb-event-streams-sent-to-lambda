"""Module for the main FilterDynamodbEventStreamsSentToLambda Stack."""

# Third party imports
from aws_cdk import core as cdk

# Local application/library specific imports
from filter_dynamodb_event_streams_sent_to_lambda.sqs_example import SqsExample
from filter_dynamodb_event_streams_sent_to_lambda.ddb_example import DdbExample


class FilterDynamodbEventStreamsSentToLambdaStack(cdk.Stack):
    """The FilterDynamodbEventStreamsSentToLambda Stack."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        """Construct a new FilterDynamodbEventStreamsSentToLambdaStack."""
        super().__init__(scope, construct_id, **kwargs)

        SqsExample(scope=self, construct_id="SqsExample")
        DdbExample(scope=self, construct_id="DdbExample")
