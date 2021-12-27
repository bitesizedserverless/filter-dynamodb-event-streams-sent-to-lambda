"""Module for the main FilterDynamodbEventStreamsSentToLambda Stack."""

# Standard library imports
# -

# Related third party imports
# -

# Local application/library specific imports
from aws_cdk import core as cdk


class FilterDynamodbEventStreamsSentToLambdaStack(cdk.Stack):
    """The FilterDynamodbEventStreamsSentToLambda Stack."""

    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        config: dict,  # pylint: disable=unused-argument
        **kwargs,
    ) -> None:
        """Construct a new FilterDynamodbEventStreamsSentToLambdaStack."""
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
