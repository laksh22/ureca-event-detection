# If not within 3*Standard Deviation
def detect_event(value, median_value, mad):
    z_value = 0.6745*(value-median_value)/mad
    threshold = 3.5
    if(z_value > threshold):
        return True
    else:
        return False