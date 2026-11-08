from pydantic import BaseModel, Field

class Answer(BaseModel):
    """
    Represents an answer to a question.
    """
    answer: str = Field(description="the answer that is needed for the user question")
    conversation: float = Field( description="This is an indicator  to know if the conversation "\
    "should still continue or no. if the agent has made the decision about the refund this should be falsse "\
    "if the converstaion is still ongoing this should be true",default=True)

class PurchaseItem(BaseModel):
    """
    Represents a single item a user has purchased.
    """
    name: str = Field(description="name of the purchased item")
    price: float = Field(description="price paid for the item")
    date: str = Field(description="purchase date, e.g. 2026-10-5")
