#!/usr/bin/env python
# coding: utf-8

# $\newcommand{\ket}[1]{\left|#1\right>}$
# 
# $\newcommand{\bra}[1]{\left<#1\right|}$
# 
# $\newcommand{\braket}[2]{\left<#1 | #2\right>}$
# 
# $\newcommand{\expectation}[1]{\left<#1\right>}$
# 

# # Entanglement and Bell tests
# 
# For this notebook, I have tried to integrate the content of IBM Q tutorial with some wikipedia examples: 
# 
# https://quantum-computing.ibm.com/docs/guide/mult-entang/entanglement-and-bell-tests <br>
# https://es.wikipedia.org/wiki/Teorema_de_Bell
# 
# One of the most interesting but at the same time counterintuitive features of quantum mechanics, is that it states that two systems which are put and kept in a coherent (entangled) state can behave in a strongly correlated way, even if they are too far apart to let any classical local theory explaining that.
# 
# Of course, this fact influences the behaviour of quantum computers, so that we can verify it and see its effect.

# ## The Bell test
# 
# To understand how entanglement prevents quantum mechanics from being a local and realist theory, we will proceed by setting up an experiment which works in classical mechanics, but fails in quantum mechanics.
# 
# It is known as the Bell test and we will present it in terms of qbits and measurement of their states, while originally we would have to deal with electrons and measurement of their spins, since it is equivalent and it keeps us in the quantum computing environment.

# ### Experimental setup
# 
# Let's suppose we prepare two qbits in a coherent state as for example:
# 
# $\ket{\psi} = \dfrac{\ket{00} + \ket{11}}{\sqrt{2}}$
# 
# If we measure the two qbits along the same *direction* (remember the Bloch sphere and the fact that the z-axis connects the $\ket{0}$ and $\ket{1}$ states), we will always get the same results for both qbits.
# In other words, if perform measurement to see if the first qbit is in the $\ket{0}$ state and we get a positive result, also the measurement of the second qbit state will give a positive result.
# This is valid not only for measurements along the z-axis, but along any axis of the Bloch sphere, the important thing is that we have to measure both the qbits along the same axis.
# 
# As a summary, the results of the measurements of the two qbits, if performed along the same axis, are fully correlated (correlation = +1).
# 
# Now, let's change a bit our measurements: the axes along which we measure the states of the two qbits will now be othogonal to each other.
# For example, if we measure the state of the first qbit along the z axis, we measure the state of the second qbit along the x axis. This is equivalent to measure if the first qbit is in the $\ket{0}$ state and if the second qbit is in the $\ket{+} = \dfrac{\ket{0} + \ket{1}}{\sqrt{2}}$ state.
# In this case, the result of the measurement of the first qbit state will not ensure anything about the state of the second qbit. So that, if we measure the first qbit to be in the $\ket{0}$ state, the second qbit may be in the $\ket{+}$ state or not, with 50% probability.
# 
# So, the results of the measurements of the two qbits, if performed along two othogonal axes, are not correlated (correlation = 0).
# 
# Up to this point, everything can be explained by the existence of hidden variables that makes it possible to have always fully correlated results when the measurement is made on the same axis for the two qbits and uncorrelated results when the measurement is performed on orthogonal axes.
# We call them *hidden* variables since we don't have direct acces to them: when we perform a measurement, we just see the result of (indirectly) setting them to the *correct* values in the prepation of the entangled state.
# 
# Since all the information needed by the qbits is, in our current assumption, stored in some hidden variable, we are now assuming quantum mechanics is a local and realist theory:
# - realism: all observables have a definite value independent of the measurement;
# - locality: no information can travel faster than the speed of light.
# 
# It is easy to understand that the results of our measurement depend (under our current assumption) on the state of the hidden variables, so that if we were able to know their state (which we can't!) we would know the outcome of the measurement *before* performing it (realism) so that the qbits do not have to *communicate* with each other to agree on the result of the measurement (locality). 

# ### The Clauser-Horne-Shimony-Holt inequality
# 
# Let's now consider another slightly different experimental setup: 
# - instead of measuring only one direction, each qbit state can be measured along two orthogonal directions (e.g. the first qbit can be measured along z-axis or along x-axis, so we can measure if it is in the $\ket{0}$ or if it is in the $\ket{+}$ state);
# - the set of axes along which we measure two different qbits are rotated by 45$^{\circ}$ with respect to each other. So, if the two axes we choose for measuring the first qbits are the z-axis (vertical axis) and the x-axis (horizontal axis), the two axes we use for measuring the second qbits are the ones shown in the following Figure.

# <img src='Bell.png'>

# What we want to do now is to choose one of the two axes for the first qbit measurement, one of the two axes for the second qbit measurement, and measure their states along those axes.
# 
# Now let's define a set of scores:
# - $\expectation{AB}$: measurement of 1st qbit along z-axis ($A$) and second qbit along 45$^{\circ}$-axis ($B$) is the same: +1 (-1 if different);
# - $\expectation{AB'}$: measurement of 1st qbit along z-axis ($A$) and second qbit along 135$^{\circ}$-axis ($B'$) is the same: +1 (-1 if different);
# - $\expectation{A'B}$: measurement of 1st qbit along x-axis ($A'$) and second qbit along 45$^{\circ}$-axis ($B$) is the same: +1 (-1 if different);
# - $\expectation{A'B'}$: measurement of 1st qbit along x-axis ($A'$) and second qbit along 135$^{\circ}$-axis ($B'$) is the same: +1 (-1 if different).
# 
# Clauser, Horne, Shimony, and Holt (CHSH) demonstrated that assuming realism and locality, then the following inequality must be true:
# 
# $ |C| = |\expectation{AB} + \expectation{AB'} + \expectation{A'B} - \expectation{A'B'}| \leq 2$
# 
# Let's verify it in our case combining all the possible outcomes of our measurements, again considering that some hidden variables have been given some particular values when we created the entanglement between our two qbits, so that realism and locality are satisfied.
# 
# In the following tables, we are going to list all the possible results we can get, and the corresponding values of C. 

# | Hidden variables states             |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
# |:------------------------------------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
# | $A$: z-axis (1st qbit)              | + | + | + | + | − | − | − | − | + | + | + | + | − | − | − | − |
# | $B$: 45$^{\circ}$-axis (2nd qbit)   | + | + | + | − | − | − | − | + | + | − | − | − | + | + | + | − |
# | $A'$: x-axis (1st qbit)             | + | + | − | − | − | − | + | + | − | + | + | − | + | − | − | + |
# | $B'$: 135$^{\circ}$-axis (2nd qbit) | + | − | − | − | − | + | + | + | + | + | − | + | − | + | − | − |

# | Score                 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
# |:----------------------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
# | $\expectation{AB}$    | +1 | +1 | +1 | −1 | +1 | +1 | +1 | -1 | +1 | −1 | −1 | −1 | −1 | −1 | −1 | +1 |
# | $\expectation{A'B}$   | +1 | +1 | −1 | +1 | +1 | +1 | −1 | +1 | −1 | −1 | −1 | +1 | +1 | −1 | −1 | −1 |
# | −$\expectation{A'B'}$ | −1 | +1 | −1 | −1 | −1 | +1 | −1 | −1 | +1 | −1 | +1 | +1 | +1 | +1 | −1 | +1 |
# | $\expectation{AB'}$   | +1 | −1 | −1 | −1 | +1 | −1 | −1 | −1 | +1 | +1 | −1 | +1 | +1 | −1 | +1 | +1 |
# | $C$                   | +2 | +2 | −2 | −2 | +2 | +2 | −2 | −2 | +2 | −2 | −2 | +2 | +2 | −2 | −2 | +2 |

# So, everything looks ok: we assumed that the strange results of entangled systems can be explained by the existence of hidden variables that, whatever they are, makes it possible to satisfy the CHSH inequality and respect locality and realism.

# ### Quantum mechanical approach
# 
# Now, let's try to solve the same problem using quantum mechanics.
# 
# As we know, in quantum mechanics the measurement process has an active role, as the act of measuring the state of a system makes it collapse to one of the possible final state, with a probability equal to the square module of the corresponding coefficient. In case the results of quantum mechanics are different from those we got in the previous section, it means that quantum mechanics is not a realist or a local theory.
# 
# In that case, we can use our quantum computer to test which one of the two approaches to the solution of our problem better adjusts to reality. 
# This highlights an interesting features of quantum computers: they represent unique tools to test quantum mechanics.
# 
# It is worth at this point taking some time to understand the meaning of the scores defined earlier.
# Each of the score represent the correlation between the two measurements and in fact, it takes value +1 when the measurements give the same result (so they are fully correlated) and it takes value -1 when the results are opposite (and they are fully uncorrelated).
# 
# In quantum mechanics, we can get the expected correlation between the measurements of two entangled qbits by calculating the expectation value $\bra{\psi} A \ket{\psi}$ of a measurement.

# So let's start preparing everything we need to solve the problem.
# 
# First of all, our two qbits, as already said, are in the following entangled state:
# 
# $\ket{\psi} = \dfrac{\ket{00} + \ket{11}}{\sqrt{2}}$
# 
# For the first qbit, we have two possibilities:
# - measure its state along the z-axis or, equivalently, measure if it is in the $\ket{0}$ state;
# - measure its state along the x-axis or, equivalently, measure if it is in the $\ket{+}$ state.
# 
# So, we recall the matrix expression of the Z and X operators:
# 
# $ Z =   
# \begin{bmatrix}
#     1 & 0 \\
#     0 & -1 
# \end{bmatrix}
# $
# 
# $ X =   
# \begin{bmatrix}
#     0 & 1 \\
#     1 & 0 
# \end{bmatrix} 
# $

# While for the second qbit, the two axes along which we want to perform the measurements are rotated by 45$^{\circ}$ with respect to the axes of the first qbit. The operators we need for these measurements can be written as:
# 
# $ W = \dfrac{Z + X}{\sqrt{2}} =   
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     1 & 1 \\
#     1 & -1 
# \end{bmatrix}
# $
# 
# $ V = \dfrac{Z - X}{\sqrt{2}} =   
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     1 & -1 \\
#     -1 & -1 
# \end{bmatrix}
# $
# 
# Remembering that each operator acts only on the corresponding qbit, independently on the other one, we can list all the possible results we can get:

# #### measurement of the state of the first qbit along the z-axis
# 
# $Z \ket{0} = 
# \begin{bmatrix}
#     1 & 0 \\
#     0 & -1 
# \end{bmatrix}
# \begin{bmatrix}
#     1 \\
#     0 
# \end{bmatrix} = 
# \begin{bmatrix}
#     1 \\
#     0 
# \end{bmatrix} = 
# \ket{0}
# $
# 
# $Z \ket{1} = 
# \begin{bmatrix}
#     1 & 0 \\
#     0 & -1 
# \end{bmatrix}
# \begin{bmatrix}
#     0 \\
#     1 
# \end{bmatrix} =
# \begin{bmatrix}
#     0 \\
#     -1 
# \end{bmatrix} = 
# - \ket{1}
# $

# #### measurement of the state of the first qbit along the x-axis
# 
# $X \ket{0} = 
# \begin{bmatrix}
#     0 & 1 \\
#     1 & 0 
# \end{bmatrix}
# \begin{bmatrix}
#     1 \\
#     0 
# \end{bmatrix} = 
# \begin{bmatrix}
#     0 \\
#     1 
# \end{bmatrix} = 
# \ket{1}
# $
# 
# $X \ket{1} = 
# \begin{bmatrix}
#     0 & 1 \\
#     1 & 0 
# \end{bmatrix}
# \begin{bmatrix}
#     0 \\
#     1 
# \end{bmatrix} =
# \begin{bmatrix}
#     1 \\
#     0 
# \end{bmatrix} = 
# \ket{0}
# $

# #### measurement of the state of the second qbit along the w-axis
# 
# $W \ket{0} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     1 & 1 \\
#     1 & -1 
# \end{bmatrix}
# \begin{bmatrix}
#     1 \\
#     0 
# \end{bmatrix} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     1 \\
#     1 
# \end{bmatrix} = 
# \ket{+}
# $
# 
# $W \ket{1} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     1 & 1 \\
#     1 & -1 
# \end{bmatrix}
# \begin{bmatrix}
#     0 \\
#     1 
# \end{bmatrix} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     1 \\
#     -1 
# \end{bmatrix} = 
# \ket{-}
# $

# #### measurement of the state of the second qbit along the v-axis
# 
# $V \ket{0} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#      1 & -1 \\
#     -1 & -1 
# \end{bmatrix}
# \begin{bmatrix}
#     1 \\
#     0 
# \end{bmatrix} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     1 \\
#     -1 
# \end{bmatrix} = 
# \ket{-}
# $
# 
# $V \ket{1} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#      1 & -1 \\
#     -1 & -1 
# \end{bmatrix}
# \begin{bmatrix}
#     0 \\
#     1 
# \end{bmatrix} = 
# \dfrac{1}{\sqrt{2}}
# \begin{bmatrix}
#     -1 \\
#     -1 
# \end{bmatrix} = 
# -\ket{+}
# $

# ### Getting the scores
# 
# Before moving to the scores, let's change a bit the notation for the two-qbits state and make clearer, for every state, to which qbit it refers:
# 
# $\ket{\psi} = \dfrac{\ket{00} + \ket{11}}{\sqrt{2}} = 
# \dfrac{\ket{0}_1 \otimes \ket{0}_2 + \ket{1}_1 \otimes \ket{1}_2}{\sqrt{2}}
# $
# 
# where the substript indicates to which qbit the state refers to and the $\otimes$ symbol underlines the fact that each operator acts only on the state associated to its qbit, leaving the state of the other untouched.

# #### $\expectation{AB}$ score
# 
# $\expectation{AB} = \bra{\psi} Z_1 W_2 \ket{\psi} =
# %
# \bra{\psi} \dfrac{Z_1 \ket{0}_1 \otimes W_2 \ket{0}_2 + Z_1 \ket{1}_1 \otimes W_2 \ket{1}_2}{\sqrt{2}} = 
# %
# \bra{\psi} \dfrac{\ket{0}_1 \otimes \ket{+}_2 + (-\ket{1}_1) \otimes \ket{-}_2}{\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{0}_1 \otimes
# \left( \dfrac{\ket{0}_2 + \ket{1}_2}{\sqrt{2}} \right) - 
# \ket{1}_1 \otimes 
# \left( \dfrac{\ket{0}_2 - \ket{1}_2}{\sqrt{2}} \right)}
# {\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{0}_1 \otimes \ket{0}_2 + 
# \ket{0}_1 \otimes \ket{1}_2 - 
# \ket{1}_1 \otimes \ket{0}_2 + 
# \ket{1}_1 \otimes \ket{1}_2}
# {2} = 
# %
# \bra{\psi} 
# \dfrac{\ket{00} + \ket{01} - \ket{10} + \ket{11}}{2} = 
# %
# \left[
# \dfrac{\bra{00} + \bra{11}}{\sqrt{2}} 
# \right]
# \left[
# \dfrac{\ket{00} + \ket{01} - \ket{10} + \ket{11}}{2} 
# \right] = \dfrac{1 + 1}{2\sqrt{2}} = \dfrac{1}{\sqrt{2}}
# $

# #### $\expectation{AB'}$ score
# 
# $\expectation{AB'} = \bra{\psi} Z_1 V_2 \ket{\psi} =
# %
# \bra{\psi} \dfrac{Z_1 \ket{0}_1 \otimes V_2 \ket{0}_2 + Z_1 \ket{1}_1 \otimes V_2 \ket{1}_2}{\sqrt{2}} = 
# %
# \bra{\psi} \dfrac{\ket{0}_1 \otimes \ket{-}_2 + (-\ket{1}_1) \otimes (-\ket{+}_2)}{\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{0}_1 \otimes
# \left( \dfrac{\ket{0}_2 - \ket{1}_2}{\sqrt{2}} \right) + 
# \ket{1}_1 \otimes 
# \left( \dfrac{\ket{0}_2 + \ket{1}_2}{\sqrt{2}} \right)}
# {\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{0}_1 \otimes \ket{0}_2 - 
# \ket{0}_1 \otimes \ket{1}_2 + 
# \ket{1}_1 \otimes \ket{0}_2 + 
# \ket{1}_1 \otimes \ket{1}_2}
# {2} = 
# %
# \bra{\psi} 
# \dfrac{\ket{00} - \ket{01} + \ket{10} + \ket{11}}{2} = 
# %
# \left[
# \dfrac{\bra{00} + \bra{11}}{\sqrt{2}} 
# \right]
# \left[
# \dfrac{\ket{00} - \ket{01} + \ket{10} + \ket{11}}{2} 
# \right] = \dfrac{1 + 1}{2\sqrt{2}} = \dfrac{1}{\sqrt{2}}
# $

# #### $\expectation{A'B}$ score
# 
# $\expectation{A'B} = \bra{\psi} X_1 W_2 \ket{\psi} =
# %
# \bra{\psi} \dfrac{X_1 \ket{0}_1 \otimes W_2 \ket{0}_2 + X_1 \ket{1}_1 \otimes W_2 \ket{1}_2}{\sqrt{2}} = 
# %
# \bra{\psi} \dfrac{\ket{1}_1 \otimes \ket{+}_2 + \ket{0}_1 \otimes \ket{-}_2}{\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{1}_1 \otimes
# \left( \dfrac{\ket{0}_2 + \ket{1}_2}{\sqrt{2}} \right) + 
# \ket{0}_1 \otimes 
# \left( \dfrac{\ket{0}_2 - \ket{1}_2}{\sqrt{2}} \right)}
# {\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{1}_1 \otimes \ket{0}_2 + 
# \ket{1}_1 \otimes \ket{1}_2 + 
# \ket{0}_1 \otimes \ket{0}_2 - 
# \ket{0}_1 \otimes \ket{1}_2}
# {2} = 
# %
# \bra{\psi} 
# \dfrac{\ket{10} + \ket{11} + \ket{00} - \ket{01}}{2} = 
# %
# \left[
# \dfrac{\bra{00} + \bra{11}}{\sqrt{2}} 
# \right]
# \left[
# \dfrac{\ket{10} + \ket{11} + \ket{00} - \ket{01}}{2} 
# \right] = \dfrac{1 + 1}{2\sqrt{2}} = \dfrac{1}{\sqrt{2}}
# $

# #### $\expectation{A'B'}$ score
# 
# $\expectation{A'B'} = \bra{\psi} X_1 V_2 \ket{\psi} =
# %
# \bra{\psi} \dfrac{X_1 \ket{0}_1 \otimes V_2 \ket{0}_2 + X_1 \ket{1}_1 \otimes V_2 \ket{1}_2}{\sqrt{2}} = 
# %
# \bra{\psi} \dfrac{\ket{1}_1 \otimes \ket{-}_2 + \ket{0}_1 \otimes (- \ket{+}_2)}{\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{1}_1 \otimes
# \left( \dfrac{\ket{0}_2 - \ket{1}_2}{\sqrt{2}} \right) + 
# \ket{0}_1 \otimes 
# \left( -\dfrac{\ket{0}_2 + \ket{1}_2}{\sqrt{2}} \right)}
# {\sqrt{2}} = 
# %
# \bra{\psi} 
# \dfrac{\ket{1}_1 \otimes \ket{0}_2 - 
# \ket{1}_1 \otimes \ket{1}_2 - 
# \ket{0}_1 \otimes \ket{0}_2 - 
# \ket{0}_1 \otimes \ket{1}_2}
# {2} = 
# %
# \bra{\psi} 
# \dfrac{\ket{10} - \ket{11} - \ket{00} - \ket{01}}{2} = 
# %
# \left[
# \dfrac{\bra{00} + \bra{11}}{\sqrt{2}} 
# \right]
# \left[
# \dfrac{\ket{10} - \ket{11} - \ket{00} - \ket{01}}{2} 
# \right] = \dfrac{-1 -1}{2\sqrt{2}} = -\dfrac{1}{\sqrt{2}}
# $

# ### Finally, the value of CHSH inequality
# 
# If we now recall the definition of the CHSH inequality, we see:
# 
# $ 
# |C| = |\expectation{AB} + \expectation{AB'} + \expectation{A'B} - \expectation{A'B'}| =
# | \dfrac{1}{\sqrt{2}} + \dfrac{1}{\sqrt{2}} + \dfrac{1}{\sqrt{2}} - \left(- \dfrac{1}{\sqrt{2}}\right)| = 
# \dfrac{4}{\sqrt{2}} = 2 \sqrt{2} > 2
# $
# 
# Which means that quantum mechanics does not respect the requirements needed by a theory to be realist and local.
# This means that, if with our quantum computer agrees with quantum mechanics, we have to accept that no hidden variables can explain our results, that the act of measuring the state of our qbits make them *choose together* the outcome.  
