'''
The process_event_log function takes the event log and turns it into a readable history.
It will present logged data in a way that is easy to understand and provides insights into the history of the tribes.
It will also be user-facing output text that will be readable
'''
def process_event_log(event_log: list[str]) -> None:
    for event in event_log:
        if event:
            print(event)