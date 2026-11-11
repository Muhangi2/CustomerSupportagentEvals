import os
import sys
from  pathlib import Path
from uuid import uuid4

# The local judge model is slow, so give each judge call up to 5 minutes.
# Must be set before deepeval is imported.
os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "300")

sys.path.insert(
0, str(Path(__file__).resolve().parent.parent / "agent")
)

from agent import agent
from dataset import dataset
from model import eval_model


from deepeval.metrics import PlanAdherenceMetric
from deepeval.integrations.langchain import CallbackHandler
from deepeval.evaluate import AsyncConfig



task_completion = PlanAdherenceMetric(
    threshold=0.8,
    # task=SUCCESSFUL_TASK_DESCRIPTION,
    model=eval_model,
    include_reason=True,
    # async_mode=False,
)

# Run test cases one at a time so they don't compete for the local model.
for golden in dataset.evals_iterator(async_config=AsyncConfig(run_async=False)):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": golden.input}]},
        config={
            "configurable": {"thread_id": str(uuid4())},
            "callbacks": [CallbackHandler()],
        },
    )


