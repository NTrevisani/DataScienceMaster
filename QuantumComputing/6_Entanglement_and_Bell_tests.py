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
# To understand how entanglement prevents quantum mechanics from being a local theory, we will proceed by setting up an experiment which works in classical mechanics, but fails in quantum mechanics.
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
# 
# Up to this point, everything can be explained by the existence of hidden variables that makes it possible to have always fully correlated results when the measurement is made on the same axis for the two qbits. 
# On the other hand, these variables are not able to give any correlation on results extracted from measurements performed on orthogonal axes.
# We call them *hidden* variables since we don't have direct acces to them, we just see the result of (indirectly) setting them to the *correct* values, through the prepation of the entangled state.

# ### The Clauser-Horne-Shimony-Holt inequality
# 
# Let's now consider another slightly different experimental setup: 
# - instead of measuring only one direction, each qbit state can be measured on two orthogonal direction (e.g. the first qbit can be measured along z-axis or along x-axis, so we can measure if it is in the $\ket{0}$ or if it is in the $\ket{+}$ state);
# - the axis along which we measure two different qbits are rotated by 45$^{\circ}$. So, if the two axes we choose for measuring the first qbits are the z-axis (vertical axis) and the x-axis (horizontal axis), the two axis we use for measuring the second qbits are the ones shown in the following Figure.  

# <img src='Bell.png'>

# What we want to do now is to choose one of the two axes for the first qbit measurement, on of the two axes for the second qbit measurement, and measure their states along those axes.
# 
# Now let's define a set of scores:
# - $\expectation{AB}$: measurement of 1st qbit along z-axis ($A$) and second qbit along 45$^{\circ}$-axis ($B$) is the same: +1 (-1 if different);
# - $\expectation{AB'}$: measurement of 1st qbit along z-axis ($A$) and second qbit along 135$^{\circ}$-axis ($B'$) is the same: +1 (-1 if different);
# - $\expectation{A'B}$: measurement of 1st qbit along x-axis ($A'$) and second qbit along 45$^{\circ}$-axis ($B$) is the same: +1 (-1 if different);
# - $\expectation{A'B'}$: measurement of 1st qbit along x-axis ($A'$) and second qbit along 135$^{\circ}$-axis ($B'$) is the same: +1 (-1 if different).
# 
# Clauser, Horne, Shimony, and Holt demonstrated that assuming:
# - realism: all observables have a definite value independent of the measurement;
# - locality: no information can travel faster than the speed of light.
# 
# Then, the following inequality must be true:
# 
# $ |C| = |\expectation{AB} - \expectation{AB'} + \expectation{A'B} + \expectation{A'B'}| \leq 2$
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
# | $\expectation{A'B'}$  | +1 | −1 | +1 | +1 | +1 | −1 | +1 | +1 | −1 | +1 | −1 | −1 | −1 | −1 | +1 | −1 |
# | −$\expectation{AB'}$  | −1 | +1 | +1 | +1 | −1 | +1 | +1 | +1 | −1 | −1 | +1 | −1 | −1 | +1 | −1 | −1 |
# | $C$                   | +2 | +2 | +2 | +2 | +2 | +2 | +2 | +2 | −2 | −2 | −2 | −2 | −2 | −2 | −2 | −2 |

# 

# In[ ]:




