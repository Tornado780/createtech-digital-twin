def calculate_costs(planned_days, predicted_days, cost_per_day=1.5):
    delay_days = predicted_days - planned_days
    cost_overrun = max(delay_days, 0) * cost_per_day
    return delay_days, cost_overrun

def risk_level(delay):
    if delay < 3:
        return "Low Risk"
    elif delay < 7:
        return "Medium Risk"
    else:
        return "High Risk"