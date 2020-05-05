#!/usr/bin/env python
# coding: utf-8

# $\newcommand{\ket}[1]{\left|#1\right>}$
# 
# $\newcommand{\bra}[1]{\left<#1\right|}$
# 
# $\newcommand{\braket}[2]{\left<#1 | #2\right>}$

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
