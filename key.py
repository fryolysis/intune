import numpy as np
import scipy.linalg
from scipy.stats import zscore

from dataclasses import dataclass
from typing import List

def deduce_key(score):
    # compute pitch class distribution
    distrib = np.zeros(12)
    for n in score:
        distrib[n.semitones%12] += n.end - n.start
    
    f = KeyEstimator()
    major, minor = f(distrib)
    x = list(enumerate(list(major) + list(minor)))
    x.sort(key=lambda t:t[1])
    res = x[-1][0]%12
    print('Deduced key (C is 0):', res)
    return res

@dataclass
class KeyEstimator:

    # adapted from:
    # https://gist.github.com/bmcfee/1f66825cef2eb34c839b42dddbad49fd

    major = np.asarray(
        [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
    )
    minor = np.asarray(
        [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
    )

    def __post_init__(self):
        self.major = zscore(self.major)
        self.major_norm = scipy.linalg.norm(self.major)
        self.major = scipy.linalg.circulant(self.major)

        self.minor = zscore(self.minor)
        self.minor_norm = scipy.linalg.norm(self.minor)
        self.minor = scipy.linalg.circulant(self.minor)

    def __call__(self, x: np.array) -> List[np.array]:

        x = zscore(x)
        x_norm = scipy.linalg.norm(x)

        coeffs_major = self.major.T.dot(x) / self.major_norm / x_norm
        coeffs_minor = self.minor.T.dot(x) / self.minor_norm / x_norm

        return coeffs_major, coeffs_minor