# InTune
This program is intended to make written music more in tune. Input is a single track midi file and the output is a modified midi file which is fine-tuned using the pitch bend feature of midi standard.

## Background
The defacto tuning for almost all contemporary western music is 12 tone equal temperament. While being a good solution to the temperament problem, its widespread adoption was heavily influenced by the fact that certain instruments are hard and very slow to tune, which makes it impossible to tune them in real-time during the performance and intractable between different musical pieces. The most famous example is probably the piano.
InTune aims to address this problem. It has several modes of operation.

## Operation
1. Fixed-temperament mode:
    This mode proposes a temperament specifically tailored for a given musical score and tunes the score to it. It accepts a score in midi format and outputs two files. One of them is the scale file in .scl format and the other one is the input score retuned to the scale given in the first file.
2. Variable tuning mode:
    This mode takes a score in midi format and outputs a retuned version of it.


## Loss function
The problem is easy enough to be solved analytically. There are 12 pitch classes that repeats over and over again. Let us represent them with integers 0-11. Let $x_i$ denote the exact interval between pitch classes $i$ and $i+1$ in cents for all $0 \le i \le 10$. Let $f$ be the function that maps the distance between two pitch classes in semitones to the ideally wanted cent value. Let $k_{ij}$ denotes the weight associated with pitch class pair $i,j$ and let $k_i$ denotes the weight associated with a distance in semitones. We define our loss function to be:

$$ L = \sum_{i=0}^11 \sum_{j=i+1}^11 k_{i,j}k_{j-i}(f(j-i) - \sum_{k=i}^{j-1} x_k)^2 $$