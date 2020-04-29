#!/usr/bin/env python
# coding: utf-8

# $\newcommand{\ket}[1]{\left|#1\right>}$
# 
# $\newcommand{\bra}[1]{\left<#1\right|}$
# 
# $\newcommand{\braket}[2]{\left<#1 | #2\right>}$

# # Decoherence
# 
# Everything here is taken from the IBM quantum computing User Guide and introduction to quantum computing:
# 
# https://quantum-computing.ibm.com/docs/guide/wwwq/decoherence

# The presence of noise in the environment surrounding the qbit can induce a loss of information, also called *decoherence*.
# 
# This makes the *pure states* we described until now to become *mixed states*.
# 
# While pure states can be represented as vectors of unit length that touch the Bloch sphere surface, the mixed states are *shorter* and stay inside the Bloch sphere.
# 
# Additionally, while pure states can be represented in density matrix form as:
# 
# $\rho =  \ket{\psi} \bra{\psi}$
# 
# mixed states are expressed as linear combinations of pure states:
# 
# $\rho =  \sum_k p_k \ket{\psi_k} \bra{\psi_k}$
# 
# We are going to see two processes that can induce decoherence:
# - Energy relaxation 
# - Dephasing

# ## Energy Relaxation and $T_1$
# 
# Qbits in the excited state $\ket{1}$ tend to go back to the fundamental state $\ket{0}$, with a time constant $T_1$. The largest the time constant, the more stable a qbit is.
# 
# To measure $T_1$, we can create several circuits in which we put a qbit in the $\ket{1}$ state, then one or more identity gates (which do nothing more than wait) and measure its state. An example of code to do this follows.

# In[1]:


# t1.py
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, execute, IBMQ

provider = IBMQ.load_account()


# In[2]:


# Build the circuits
pre = QuantumCircuit(1, 1)
pre.x(0)
pre.barrier()
meas = QuantumCircuit(1, 1)
meas.measure(0, 0)
circuits = []
exp_vector = range(1,51)
for exp_index in exp_vector:
    middle = QuantumCircuit(1, 1)
    for i in range(45*exp_index):
        middle.iden(0)
    circuits.append(pre + middle + meas)


# In[3]:


from qiskit.visualization import plot_histogram

# Draw the first circuit
# this is the one with less Id gates,
# or the one that takes less time to measure the qbit state
circuits[0].draw(output='mpl')


# In[4]:


# Execute the circuits
shots = 1024

# Select the backend (in this case, the ibmq_rome quantum computer)
# Here we are not doing a simulation, but measuring the T1 of this particular real quantum computer!
backend = provider.get_backend('ibmq_rome')
job = execute(circuits, backend, shots=shots)
result = job.result()


# In[8]:


# Plot the result
exp_data = []
exp_error = []
for idx, _ in enumerate(exp_vector):
    data = result.get_counts(idx)
    try:
        p0 = data['0']/shots
    except KeyError:
        p0 = 0
    exp_data.append(1 - p0)
    exp_error.append(np.sqrt(p0*(1-p0)/shots))

plt.errorbar(exp_vector, exp_data, exp_error)
plt.xlabel('time [45*gate time]')
plt.ylabel('Pr(1)')
plt.grid(True)


# ## Dephasing and $T_2$
# 
# Dephasing is a process that affects qbits in superposition status, as for example:
# 
# $\ket{+} = \dfrac{\ket{0} + \ket{1}}{\sqrt{2}}$
# 
# It consists in a rotation along the Z axis (or, equivalently, in the XY plane) of the vector state, if we consider the Bloch Sphere representation.
# 
# Depending on the way we measure it, its time constant goes under the name of $T_2$ or $T_2^*$.
# 
# A good reference to understand the differences between $T_2$ or $T_2^*$ is: <br>
# https://quantumcomputing.stackexchange.com/questions/2432/whats-the-difference-between-t2-and-t2
# 
# Let's see it with a couple of examples.

# ### The Ramsey Experiment: measuring $T_2^*$
# 
# In this first experiment, we will put a qbit in the $\ket{+}$ state using a H gate:
# 
# $\ket{\psi} = H \ket{0} = \ket{+} = \dfrac{\ket{0} + \ket{1}}{\sqrt{2}}$
# 
# Then, we wait a certain time $\Delta t$, so that the state evolves as:
# 
# $\ket{\psi} = \dfrac{\ket{0} + e^{-i \Delta t}\ket{1}}{\sqrt{2}} = 
# \dfrac{\ket{+} + \ket{-} + e^{-i \Delta t}\ket{+} - e^{-i \Delta t} \ket{-}}{2} = 
# \dfrac{(1 + e^{-i \Delta t}) \ket{+} + (1 - e^{-i \Delta t}) \ket{-}}{2}$
# 
# This means that, after a time interval $\Delta t$, the probability of being in the state $\ket{+}$ is:
# 
# $ |\braket{+}{\psi}|^2 = \dfrac{|(1 + e^{-i \Delta t})|^2}{4} = 
# \cos^2(\dfrac{\Delta t}{2}) = \dfrac{1 + \cos(\Delta t)}{2}$

# But we can only measure the state of a qbit in the computational base ($\ket{0}, \ket{1}$), so we ue a trick: we apply again a H gate:
# 
# $H \ket{\psi} =  \dfrac{H \ket{0} + e^{-i \Delta t} H \ket{1}}{\sqrt{2}} = 
# \dfrac{\ket{+} + e^{-i \Delta t} \ket{-}}{\sqrt{2}} = 
# \dfrac{\ket{0} + \ket{1} + e^{-i \Delta t}(\ket{0} - \ket{1})}{2} = 
# \dfrac{(1 + e^{-i \Delta t})\ket{0} + (1 - e^{-i \Delta t})\ket{1}}{2}$
# 
# This means that the probability of measuring $\ket{\psi} = \ket{0}$ is:
# 
# $ |\braket{0}{\psi}|^2 = \dfrac{|(1 + e^{-i \Delta t})|^2}{4} = 
# \cos^2(\dfrac{\Delta t}{2}) = \dfrac{1 + \cos(\Delta t)}{2}$
# 
# Basically, measuring the probability of being in the $\ket{0}$ state after applying a H gate is equivalent of measuring the probability of being in the $\ket{+}$ state before applying the H gate.
# 
# Let's see it with an example code:

# In[6]:


# t2_ramsey.py
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, execute

provider = IBMQ.load_account()


# In[7]:


# Build the circuits
pre = QuantumCircuit(1, 1)
pre.h(0)
pre.barrier()
meas_x = QuantumCircuit(1, 1)
meas_x.barrier()
meas_x.h(0)
meas_x.measure(0, 0)
circuits = []
exp_vector = range(1,51)
phase = 0.0
for exp_index in exp_vector:
    middle = QuantumCircuit(1, 1)
    #phase = phase + 6*np.pi/len(exp_vector)
    #middle.u1(phase,0)
    for i in range(25*exp_index):
        middle.iden(0)
    circuits.append(pre + middle + meas_x)


# In[8]:


from qiskit.visualization import plot_histogram

# Draw the first circuit
# this is the one with less Id gates,
# or the one that takes less time to measure the qbit state
circuits[0].draw(output='mpl')


# In[9]:


# Execute the circuits
shots = 1024
backend = provider.get_backend('ibmqx2')
job = execute(circuits, backend, shots=shots)
result = job.result()


# In[10]:


# Plot the result
exp_data = []
exp_error = []
for idx, _ in enumerate(exp_vector):
    data = result.get_counts(idx)
    try:
        p0 = data['0']/shots
    except KeyError:
        p0 = 0
    exp_data.append(p0)
    exp_error.append(np.sqrt(p0*(1-p0)/shots))

plt.errorbar(exp_vector, exp_data, exp_error)
plt.xlabel('time [25*gate time]')
plt.ylabel('Pr(0)')
plt.ylim(0,1)
plt.grid(True)


# Why do we see that the evolution is not exactly as we would expect (it does not go to 0)? Is it because the $\ket{1}$ state not only rotate around Z, but also tends to go toward $\ket{0}$ with time?
# 
# Maybe the following example makes the question clearer

# Alternatively, we can measure the state in the superposition basis. The original qskit tutorial does it with a trick, by applying a variable phase to the qbit state before waiting the qbit to evolve with time: 

# In[11]:


# Build the circuits
pre = QuantumCircuit(1, 1)
pre.h(0)
pre.barrier()
meas_x = QuantumCircuit(1, 1)
meas_x.barrier()
meas_x.h(0)
meas_x.measure(0, 0)
circuits = []
exp_vector = range(1,51)
phase = 0.0
for exp_index in exp_vector:
    middle = QuantumCircuit(1, 1)
    phase = phase + 6*np.pi/len(exp_vector)
    # That's the 'trick'!!
    middle.u1(phase,0)
    for i in range(5*exp_index):
        middle.iden(0)
    circuits.append(pre + middle + meas_x)


# In[12]:


from qiskit.visualization import plot_histogram

# Draw the first circuit
# this is the one with less Id gates,
# or the one that takes less time to measure the qbit state

# Here we can see that we are applying a phase before 
# applying a set of Id operators!
circuits[0].draw(output='mpl')


# In[13]:


circuits[1].draw(output='mpl')


# In[14]:


# Execute the circuits
shots = 1024
backend = provider.get_backend('ibmqx2')
job = execute(circuits, backend, shots=shots)
result = job.result()


# In[15]:


# Plot the result
exp_data = []
exp_error = []
for idx, _ in enumerate(exp_vector):
    data = result.get_counts(idx)
    try:
        p0 = data['0']/shots
    except KeyError:
        p0 = 0
    exp_data.append(p0)
    exp_error.append(np.sqrt(p0*(1-p0)/shots))

plt.errorbar(exp_vector, exp_data, exp_error)
plt.xlabel('time [5*gate time]')
plt.ylabel('Pr(+)')
plt.ylim(0,1)
plt.grid(True)


# Here we see how the probability to measure the qbit state to be $\ket{+}$ oscillates with time, which means that the qbit state is actually rotating around the Z axis of the Bloch sphere.
# 
# But we can also observe a damping of the oscillation, produced by energy relaxation: not only the $\ket{1}$ *part* of the superposition state $\ket{+}$ is rotating with time, but it is also *relaxing* toward the fundamental state $\ket{0}$.

# ### The Echo Experiment: measuring $T_2$
# 
# In the second experiment, we start again with a qbit in the $\ket{+}$ state:
# 
# $\ket{\psi} = H \ket{0} = \ket{+} = \dfrac{\ket{0} + \ket{1}}{\sqrt{2}}$
# 
# Then, instead of waiting a time $\Delta t$, we wait just $\dfrac{\Delta t}{2}$:
# 
# $\ket{\psi} = \dfrac{\ket{0} + e^{-i \frac{\Delta t}{2}}\ket{1}}{\sqrt{2}}$
# 
# After that, we apply this time a X gate:
# 
# $X \ket{\psi} =  
# \dfrac{X \ket{0} + e^{-i \frac{\Delta t}{2}} X \ket{1}}{\sqrt{2}} = 
# \dfrac{\ket{1} + e^{-i \frac{\Delta t}{2}} \ket{0}}{\sqrt{2}}$
# 
# Then we let evolve the system for another $\dfrac{\Delta t}{2}$:
# 
# $\ket{\psi} =  
# \dfrac{e^{-i \frac{\Delta t}{2}}\ket{1} + e^{-i \frac{\Delta t}{2}} \ket{0}}{\sqrt{2}} = 
# \dfrac{e^{-i \frac{\Delta t}{2}}(\ket{0} + \ket{1})}{\sqrt{2}} =
# e^{-i \frac{\Delta t}{2}}\ket{+} $
# 
# This means that in this case, the probability of measuring the state $\ket{\psi} = \ket{+}$ is:
# 
# $| \braket{+}{\psi}|^2 = |e^{-i \frac{\Delta t}{2}}|^2 = 1$
# 
# On the other hand, also in this case we are not able to measure the state in the superposition base, so we apply again a H gate:
# 
# $H \ket{\psi} =  
# \dfrac{e^{-i \frac{\Delta t}{2}}(H\ket{0} + H\ket{1})}{\sqrt{2}} =
# \dfrac{e^{-i \frac{\Delta t}{2}}(\ket{+} + \ket{-})}{\sqrt{2}} =
# e^{-i \frac{\Delta t}{2}}\ket{0} $
# 
# So that now, the probability of measuring $\ket{\psi} = \ket{0}$ is the same as measuring $\ket{\psi} = \ket{+}$ before applying the H gate, and is 1.
# 
# This means that for this configuration, the time $T_2$ is infinite.

# In[16]:


# t2_echo.py
import numpy as np
import matplotlib.pyplot as plt

from qiskit import IBMQ, QuantumCircuit, execute

provider = IBMQ.load_account()


# In[17]:


# Build the circuits
pre = QuantumCircuit(1, 1)
pre.h(0)
pre.barrier()
meas_x = QuantumCircuit(1, 1)
meas_x.barrier()
meas_x.h(0)
meas_x.measure([0], [0])
circuits = []
exp_vector = range(1,51)
for exp_index in exp_vector:
    middle = QuantumCircuit(1, 1)
    for i in range(15*exp_index):
        middle.iden(0)
    middle.x(0)
    for i in range(15*exp_index):
        middle.iden(0)
    circuits.append(pre + middle + meas_x)


# In[18]:


from qiskit.visualization import plot_histogram

# Draw the first circuit
# this is the one with less Id gates,
# or the one that takes less time to measure the qbit state
circuits[0].draw(output='mpl')


# In[19]:


# Execute the circuits
backend = provider.get_backend('ibmqx2')
job = execute(circuits, backend)
result = job.result()


# In[20]:


# Plot the result
exp_data = []
exp_error = []
for exp_index in exp_vector:
    data = result.get_counts(circuits[exp_index-1])
    try:
        p0 = data['0']/shots
    except KeyError:
        p0 = 0
    exp_data.append(p0)
    exp_error.append(np.sqrt(p0*(1-p0)/shots))

plt.errorbar(exp_vector, exp_data, exp_error)
plt.xlabel('time [31*gate time]')
plt.ylabel('Pr(0)')
plt.grid(True)


# ### Some considerations on $T_2$ and $T_2^*$

# We have seen that in both the experiments we described to measure the dephasing time constant, the results we obtained were not exactly the ones we expected.
# 
# This happens since it is not possible to isolate the effect of dephasing from the effect of energy relaxation.
# In other words, while the vector sate $\ket{\psi}$ rotates around the Z axis, its $\ket{1}$ component is still relaxing towards the fundamental $\ket{0}$ state.
# 
# To visualize this on the Bloch sphere, we can think as the vector state of a qbit in superposition does not only rotate around the equator, but also falls down to the $\ket{0}$ pole, creating a spiral.
# 
# To get the functional form of the spiral, we would need to include the energy relaxation term in the time evolution of the $\ket{\psi}$ state.
