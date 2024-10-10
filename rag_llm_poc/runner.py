import shutil
import uuid
import graph
import util
from langchain_core.messages import ToolMessage

# Let's create an example conversation a user might have with the assistant
tutorial_questions = [
    "What is CVS Health known for?",
    "Hi there, what's my claim status?",
    "Sure, my member id is A1234, and my DOB is June 9th, 1999",
    #     "Now what is my claim status for A5999",
    #     "What about B4231?",
    #     "Give me a summary of both claims",
]

# Update with the backup file so we can restart from the original place in each section
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}


_printed = set()
for question in tutorial_questions:
    events = graph.graph.stream(
        {"messages": ("user", question)}, config, stream_mode="values"
    )
    for event in events:
        util._print_event(event, _printed)
    snapshot = graph.graph.get_state(config)
    while snapshot.next:
        # We have an interrupt! The agent is trying to use a tool, and the user can approve or deny it
        # Note: This code is all outside of your graph. Typically, you would stream the output to a UI.
        # Then, you would have the frontend trigger a new run via an API call when the user has provided input.
        try:
            user_input = input(
                "Do you approve of the above actions? Type 'y' to continue;"
                " otherwise, explain your requested changed.\n\n"
            )
        except:
            user_input = "y"
        if user_input.strip() == "y":
            # Just continue
            result = graph.graph.invoke(
                None,
                config,
            )
        else:
            # Satisfy the tool invocation by
            # providing instructions on the requested changes / change of mind
            result = graph.graph.invoke(
                {
                    "messages": [
                        ToolMessage(
                            tool_call_id=event["messages"][-1].tool_calls[0]["id"],
                            content=f"API call denied by user. Reasoning: '{user_input}'. Continue assisting, accounting for the user's input.",
                        )
                    ]
                },
                config,
            )
        snapshot = graph.graph.get_state(config)
