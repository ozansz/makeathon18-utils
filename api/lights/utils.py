import math

kMaxTime = {
    "stay": 60,
    "go": 60
}

kMinTime = {
    "stay": 20,
    "go": 15
}

kJamPassStay = 10
kJamPassGo = 120

kDensityLookBackCount = 10

def sigmoid(z):
    return 1 / (1 + math.exp(-1*z))

def get_optimal_process_time(node, stay_or_go):
    mean_density = sum([d.density for d in node.density_records.order_by('-timestamp')][:5]) / kDensityLookBackCount

    if mean_density >= 1:
        if stay_or_go == "stay":
            return kJamPassStay
        elif stay_or_go == "go":
            return kJamPassGo

    if stay_or_go == "stay":
        return (kMaxTime["stay"] - kMinTime["stay"]) * (1 - mean_density) + kMinTime["stay"]
    elif stay_or_go == "go":
        return (kMaxTime["go"] - kMinTime["go"]) * mean_density + kMinTime["go"]
