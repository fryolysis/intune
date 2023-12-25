# InTune

The defacto tuning for almost all contemporary western music is 12 tone equal temperament. It is a good solution given the constraint that tuning an instrument in real-time during the performance and even between different musical pieces in a single sitting can be a tedious and time-consuming task. The most famous example is probably the piano where the tuning requires a separate profession.

We believe that 12 tone equal temperament is not necessarily the best tuning system for every melody if retuning is an easy operation like in electronic music. InTune aims to compute a better tuning tailored to a given musical piece. 

It has two modes of operation:

## Fixed Tuning Mode
This mode proposes a 12 tone (usually unequal) temperament specifically tailored for a given musical score. It assumes that the input score consists of at most 12 distinct pitches per octave, and that for at least one kind of step-interval (like 4 steps) there is a unique pure interval (like 386 cents) that is ideally desired anywhere the step-interval occurs within the score.

We use a loss function to express how good a tuning fits to a given score. The problem is easy enough to be solved analytically. There are 12 pitch classes that repeats over and over again. Let us represent them with integers from 0 to 11, where 0 corresponds to the pitch class C. Let $x_i$ denote the exact interval between pitch classes 0 and $i$ in cents for all $0 \le i \le 11$. $x_0 = 0$ by definition. Let $\tau_i$ be the ideally wanted cent value for the interval of $i$ steps. Let $\kappa_{ij}$ denotes the weight associated with pitch class pair $i,j$ and let $\kappa_i$ denotes the weight associated with an interval of $i$ steps. The loss function is really just a weighted sum of squared errors. More formally we define our loss function to be:

$$ L = \sum_{i=0}^{11} \sum_{j=i+1}^{11} \kappa_{i,j}\kappa_{j-i}\left(x_j - x_i - \tau_{j-i}\right)^2 $$

The coefficients $\kappa_{i,j}$ are intended to be computed from the input score. We implemented a weighting algorithm which gives more weight to pairs that appear close together in the score (time proximity) and pairs that appear more frequently in the score (frequency of occurrence). The user can enter parameters for window size and the importance of occurrence frequency. Thanks to [Robin](https://github.com/RobinTournemenne) for the idea.

The coefficients $\kappa_i$ are for putting emphasis on different kind of intervals.

To minimize the loss, we must compute the $x_i$ values that vanish the partial derivative of $L$ with respect to $x_i$ for each $i$. This is just a linear system of equations with 11 unknowns. If some pitch classes never appear in the score (if there are less than 12 distinct pitch classes) the system is degenerate, however we still output a 12 tone scale for convenience, using 12 tone equally tempered versions of missing pitch classes. We use SymPy to solve this problem analytically.


## Variable Tuning Mode

The algorithm we propose is a slightly modified version of the one we proposed for fixed-tuning mode:
1. Whenever a pitch class $i$ appears after a long time since its last appearance (or for the first time), introduce a new variable $x_i$ to represent pitch class $i$ from that point on, until a new sufficiently large gap occurs.
1. Use the algorithm proposed for fixed-tuning mode to compute the solution.

Note that depending on the length of the score and the aging parameter used to define "long time ago", the computational cost may be too high.

This mode has not been implemented yet.

## Does it really work?
For fixed tuning, it usually does. But when it does, it is usually quite close to the standard temperament, especially when the occurrence frequency is not important. Still, we have some examples that sound pleasant while being significantly deviated from the standard tuning. Below there is an example.

Mozart's Sonata No.8, first movement ([midi file](http://www.piano-midi.de/midis/mozart/mz_311_1.mid)):
- [Here](https://drive.google.com/file/d/1xskHf3dsV0DISakGPvwJ5pTAF7zLGVsR/view?usp=sharing) in standard 12tet tuning
- [Here](https://drive.google.com/file/d/1EtOZK-fWTnnvUyfe6NL9ttr5YLN-O2XD/view?usp=sharing) in custom tuning

Pianoteq software with identical settings except tuning is used to sound both of the samples. Here's the diagram of custom tuning drawn by Pianoteq software:

![](https://i.ibb.co/PzGgRKj/mz-311-1.png)

## Limitations and Further Work

We believe that the biggest limitation of this work is that a step interval must be assigned to the same pure interval wherever it occurs. For instance 3 steps (3 semitones if you like) always have a unique meaning independent of the context. We think that this may not be the case and we have good reasons to think so. Looking at the harmonic series, we see that especially small intervals may have several different pure interpretations. 3 steps may mean 6/5 in major/minor triads, 7/6 in diminished triads. 4 steps may mean 5/4 in major/minor triads, 9/7 and 11/9 in an augmented triad and so on.

We think that in many western classical music 5/4 and 3/2 ratios occur almost between every possible pair of notes which leaves no room for a fixed tuning to consider pure intervals of higher primes. Variable tuning scheme may benefit from including the consideration of pure intervals of higher order.
