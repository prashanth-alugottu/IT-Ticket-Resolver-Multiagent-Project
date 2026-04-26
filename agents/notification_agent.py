from autogen import AssistantAgent
from utils.llm_config import llm_config

def get_notification_agent():
    return AssistantAgent(
        name="NotificationAgent",
        system_message="You are an IT notification agent that sends alert or escalates unresolved ticket",
        llm_config=llm_config
    )
