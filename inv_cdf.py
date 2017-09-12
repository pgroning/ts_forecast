import scipy.stats as sp

# Cumulative distribution function:
# sp.norm.cdf
#
# Inverse cdf:
# sp.norm.ppf
#

def inv_cdf():
    alpha = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999]  # service levels
    for a in alpha:
        z = sp.norm.ppf(a)
        print z

    
if __name__ == "__main__":
    inv_cdf()
    
