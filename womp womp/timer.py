import time

def start_timer(hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds
    result = []
    
    for remaining in range(total_seconds, -1, -1):
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60
        result.append(f"{h} hours, {m} minutes, and {s} seconds left.")
        time.sleep(1)  # Simulates real-time countdown
    
    result.append("Timer Complete!")
    return "<br>".join(result)
