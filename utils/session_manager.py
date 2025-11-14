import pandas as pd
from datetime import datetime

def save_session(left_jump, right_jump, diff):
    data = pd.DataFrame([{
        "timestamp": datetime.now(),
        "left_jump": left_jump,
        "right_jump": right_jump,
        "diff": diff
    }])
    data.to_csv("data/sessions/log.csv", mode="a", header=True, index=False)

