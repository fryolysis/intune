# InTune
This program is intended to make written music more in tune. Input is a single track midi file and the output is a modified midi file which is fine-tuned using the pitch bend feature of midi standard.

## Background
The defacto tuning for almost all contemporary western music is 12 tone equal temperament. It is a good solution given the constraint that tuning an instrument in real-time during the performance and even between different musical pieces in a single performence can be a tedious task. The most famous example is probably the piano where the tuning requires a separate profession.

We believe that 12 tone equal temperament is not necessarily the best tuning system for every melody if retuning is an easy operation like in electronic music. InTune aims to compute a better tuning tailored to a given musical piece. It has two modes of operation.

## Operation
### Fixed-temperament mode
This mode proposes a 12 tone temperament specifically tailored for a given musical score and tunes the score to it. It accepts a score in midi format and outputs two files. One of them is the scale file in .scl format and the other one is the input score retuned to the scale given in the first file.
### Variable tuning mode
This mode takes a score in midi format and outputs a retuned version of it. Number of distinct pitches used in the score is unlimited and are chosen in order to maximize consonance in a local area of the score. This mode displays close resemblance with Turkish qanun mandal system which is a flexible tuning design allowing the player to be able to change the fine-tuning of each course of strings during the performance.

## Technical Details

### Fixed-temperament mode
For the fixed-temperament mode we use a loss function to express how good a temperament fits to a given score.

The problem is easy enough to be solved analytically. There are 12 pitch classes that repeats over and over again. Let us represent them with integers from 0 to 11. Let $x_i$ denote the exact interval between pitch classes 0 and $i$ in cents for all $0 \le i \le 11$. $x_0 = 0$ by definition. Let $\tau_i$ be the ideally wanted cent value for the interval of $i$ semitones. Let $\kappa_{ij}$ denotes the weight associated with pitch class pair $i,j$ and let $\kappa_i$ denotes the weight associated with a distance in semitones. The loss function is really just a weighted sum of squared errors. More formally we define our loss function to be:

$$ L = \sum_{i=0}^{11} \sum_{j=i+1}^{11} \kappa_{i,j}\kappa_{j-i}\left(x_j - x_i - \tau_{j-i}\right)^2 $$

The coefficients $\kappa_{i,j}$ are typically computed from the input score. The default algorithm uses the frequency of occurrences. The coefficients $\kappa_i$ are for putting emphasis on different kind of intervals. The default map assigns 1 to all consonant intervals and 0 to all the rest. Consonances are thirds, sixths, perfect fourth and fifth.

To minimize the loss, we must compute the $x_i$ values that vanish the partial derivative of $L$ with respect to $x_i$ for each $i$.

$$ \frac{\partial L}{\partial x_k} =  
2 \sum_{i=0}^{k-1} \kappa_{i,k}\kappa_{k-i} (x_k - x_i - \tau_{k-i})
-2 \sum_{j=k+1}^{11} \kappa_{k,j}\kappa_{j-k} (x_j - x_k - \tau_{j-k})
= 0$$

This is just a linear system of equations with 11 unknowns. Note that even though certain pitch class never appears in input score we still output a 12 tone scale for convenience.

We use SymPy to solve this problem analytically.