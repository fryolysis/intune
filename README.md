# InTune

The defacto tuning for almost all contemporary western music is 12 tone equal temperament. It is a good solution given the constraint that tuning an instrument in real-time during the performance and even between different musical pieces in a single sitting can be a tedious and time-consuming task. The most famous example is probably the piano where the tuning requires a separate profession.

We believe that 12 tone equal temperament is not necessarily the best tuning system for every melody if retuning is an easy operation like in electronic music. InTune aims to compute a better tuning tailored to a given musical piece. 

Here is the algorithm:
1. Assign a unique variable to each note instance in the score.
1. Write down the total cost and construct the linear system from partial derivatives of it.
1. Use SciPy's function for solving $Ax=b$ for band matrix $A$.

Let us put all notes in an ascending order w.r.t their onset time. Let $N$ be the number of notes in the score and let $\nu_i$ be the neighborhood of the $i^{th}$ note. Let $x_i$ be the final absolute cents value of $i^{th}$ note. $\tau_{i,j}$ is the desired interval between $i^{th}$ and $j^{th}$ notes in cents (the ideal value for $x_i-x_j$), and $\kappa_{i,j}$ is the weighting factor for the note pair.
$$L = \sum_{i=1}^N \sum_{j \in \nu_i} \kappa_{i,j} (x_i - x_j - \tau_{i,j})^2$$

Differentiating the loss function we get
$$\frac{\partial L}{\partial x_k} = \sum_{j \in \nu_k} 2 \kappa_{k,j} (x_k - x_j - \tau_{k,j}) + \sum_{\{i \mid k \in \nu_i\}} -2 \kappa_{i,k}(x_i - x_k - \tau_{i,k})$$

We get $N$ equations via setting all partial derivatives to 0.
$$\sum_{j \in \nu_k} \kappa_{k,j} (x_k - x_j - \tau_{k,j}) - \sum_{\{i \mid k \in \nu_i\}} \kappa_{i,k}(x_i - x_k - \tau_{i,k}) = 0$$

Since neighborhood is a symmetric relation we have $\nu_k = \set{i \mid k \in \nu_i}$. Informally this means that the neighborhood of a note $x$ and the set of all notes whose neighborhood contains $x$ are the same set. Thus, we have
$$\sum_{i \in \nu_k} \kappa_{k,i} (x_k - x_i - \tau_{k,i}) - \kappa_{i,k} (x_i - x_k - \tau_{i,k}) = 0$$

Note that $\kappa$ is a symmetric function, that is, the order of its arguments is not important. Also note that $\tau_{i,k} = - \tau_{k,i}$ for all $i,k$. Therefore we have
$$\sum_{i \in \nu_k} \kappa_{k,i} (x_k - x_i - \tau_{k,i}) = 0$$

Now we can write our problem in the form of a matrix equation $Ax=b$ where $x=(x_1,x_2,\ldots,x_N)$ is the vector of unknowns.

$$\begin{align}    A_{ij} &= \begin{cases}        \sum_{k \in \nu_i} \kappa_{i,k} &\text{if } j=i \newline        - \kappa_{i,j} &\text{if } j \in \nu_i \newline        0 &\text{else}    \end{cases} \newline    b_{i}  &= \sum_{j \in \nu_i} \kappa_{i,j} \tau_{i,j}\end{align}$$

One would typically choose a neighborhood of size less than 100, so given that the whole score typically consists of thousands of note instances, the matrix $A$ is what is called a band matrix, having non-zero elements only a thin band around its main diagonal. Solving such linear systems seems to be cheaper than arbitrary ones and thus our algorithm works pretty fast.

From our experiments, it seems like the key pitch should not be changed throughout a piece. For now, fixing the key pitch is trying to be ensured via keeping the neighborhood size large and assigning very high cost to unison deviation in case when both of notes are key. The key estimation algorithm used is [Krumhansl-Schmuckler algorithm](https://gist.github.com/bmcfee/1f66825cef2eb34c839b42dddbad49fd). In the future, we plan to address this issue in a better way.

### Criticism

The main drawback of this approach is the usage of square loss function to model a person's preference. From our experiments we think that this loss function is far from accurate, as it prefers outcomes with a few badly out-of-tune intervals and many perfectly intune intervals instead of all slightly out-of-tune intervals. We think that human perception prefers the latter scenario, so an ideal loss function should have a much higher exponent than two. To avoid high computational cost, we think of implementing the extreme case of hard constraints using simplex algorithm.

### Some results

We felt that certain classical pieces that emphasizes the sweetness of major thirds (like Mozart's Piano Sonata No. 11 in A Major, 1. Theme) sound better with major thirds closer to the pure 5/4 ratio.

