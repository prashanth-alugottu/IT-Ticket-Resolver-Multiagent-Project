from autogen import UserProxyAgent
from agent.classifier_agent import get_classifier_agent

def get_user_agent():
    user = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False,
    )
    return user


sample_tickets = [
    "My Mouse is not functioning"
]
def run_test():
    user = get_user_agent()
    classifier_agent=get_classifier_agent()

    for ticket in sample_tickets:
        print(f"\n ticket {ticket}")
        user.initiate_chat(
            recipient=classifier_agent,
            message=f"Classify this ticket {ticket}",
            max_turns=1
        )


if __name__ =="__main__":
    run_test()