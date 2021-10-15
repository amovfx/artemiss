from scipy.stats import entropy

def ball_entropy(*args):
    val = float(sum(args))
    for a in args():
