"""Define the stack for the API."""
from pathlib import Path
from aws_cdk import (
    App,
    Stack,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as _lambda_python,
)
from .base_stack import BaseStack
from .base_stack_config import StackConfigBaseModel



_CURRENT_DIR = Path(__file__).parent
_API_ENTRY_POINT = _CURRENT_DIR.parent / "api"
_TOP_LEVEL_DIR = _CURRENT_DIR.parent.parent


class APIStack(BaseStack):
    """Define the stack for the API."""

    def __init__(
        self,
        app: App,
        config: StackConfigBaseModel,
    ) -> None:
        """Initialize the stack."""
        super().__init__(scope=app, config=config)

        self._api = _lambda_python.PythonFunction(
            self,
            "api",
            entry=str(_API_ENTRY_POINT.resolve()),
            runtime=_lambda.Runtime(
                "python3.10",
                _lambda.RuntimeFamily.PYTHON,
                bundling_docker_image="public.ecr.aws/sam/build-python3.10:latest-arm64",
            ),
            index="index.py",
            handler="handler",
            architecture=_lambda.Architecture.ARM_64,
            layers=[
                _lambda_python.PythonLayerVersion(
                    self,
                    "api-dependencies",
                    entry=_TOP_LEVEL_DIR.as_posix(),
                    compatible_runtimes=[
                        _lambda.Runtime(
                            'python3.10',
                            _lambda.RuntimeFamily.PYTHON,
                            bundling_docker_image="public.ecr.aws/sam/build-python3.10:latest-arm64"
                        ),
                    ],
                    bundling=_lambda_python.BundlingOptions(
                        user="root",
                        asset_excludes=[".venv", "cdk.out"]
                    )     
                )
            ]
        )

        self._api.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allow_credentials=True,
                allowed_headers=["*"],
                allowed_origins=["*"],
            ),
            invoke_mode=_lambda.InvokeMode.BUFFERED,
        )
