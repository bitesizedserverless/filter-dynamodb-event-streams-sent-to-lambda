"""Module for the main DdbExample Construct."""

# Standard library imports
# -

# Third party imports
from aws_cdk import (
    core as cdk,
    aws_dynamodb as dynamodb,
)

# Local application/library specific imports
from filter_dynamodb_event_streams_sent_to_lambda.ddb_inserts_only import DdbInsertsOnly
from filter_dynamodb_event_streams_sent_to_lambda.ddb_insert_users import DdbInsertUsers
from filter_dynamodb_event_streams_sent_to_lambda.ddb_new_and_updated_flagged import (
    DdbNewAndUpdatedFlagged,
)


class DdbExample(cdk.Construct):
    """The DdbExample Construct."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        """
        Construct a new DdbExample.

        This Construct contains a source DynamoDB Table, a Lambda Function and
        an Event Source Mapping to connect the two.
        """
        super().__init__(scope, construct_id, **kwargs)

        # The queue that will trigger the event source mapping
        table = dynamodb.Table(
            scope=self,
            id="DynamoDBTable",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="PK", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            stream=dynamodb.StreamViewType.NEW_IMAGE,
        )

        DdbInsertsOnly(scope=self, construct_id="DdbInsertsOnly", table=table)
        DdbInsertUsers(scope=self, construct_id="DdbInsertUsers", table=table)
        DdbNewAndUpdatedFlagged(
            scope=self, construct_id="DdbNewAndUpdatedFlagged", table=table
        )
