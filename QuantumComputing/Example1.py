#!/usr/bin/env python
# coding: utf-8

# ## Example 1
# 
# Simple q-bit measurement

# In[1]:


# single_q_measurement.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer


# In[2]:


# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)


# In[3]:


# Build the circuit
single_q_measurement = QuantumCircuit(q, c)
single_q_measurement.measure(q, c)


# In[4]:


# Draw the circuit
single_q_measurement.draw()


# In[6]:


# Execute the circuit
job = execute(single_q_measurement, backend = Aer.get_backend('qasm_simulator'), shots=1024)
result = job.result()


# In[7]:


# Print the result
print(result.get_counts(single_q_measurement))


# All the results give 0 (fundamental state).

# ## Example 2
# 
# Q-bit flip circuit

# In[8]:


# excited_state.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer


# In[9]:


# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)


# In[10]:


# Build the circuit
excited_state = QuantumCircuit(q, c)
excited_state.x(q)
excited_state.measure(q, c)


# In[11]:


# Draw the circuit
excited_state.draw()


# In[12]:


# Execute the circuit
job = execute(excited_state, backend = Aer.get_backend('qasm_simulator'), shots=1024)
result = job.result()


# In[13]:


# Print the result
print(result.get_counts(excited_state))


# All the results give 1 (excited state).

# ## Example 3
# 
# Superpoistion

# In[14]:


# superposition_state.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer


# In[15]:


# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)


# In[16]:


# Build the circuit
superposition_state = QuantumCircuit(q, c)
superposition_state.h(q)
superposition_state.measure(q, c)


# In[17]:


# Draw the circuit
superposition_state.draw()


# H gate creates a superposition between fundamental state and excited state in the same q-bit:
# 
# $ |+> = \frac{| 0 > + | 1 >}{\sqrt{2}} $ 

# In[18]:


# Execute the circuit
job = execute(superposition_state, backend = Aer.get_backend('qasm_simulator'), shots=1024)
result = job.result()


# In[19]:


# Print the result
print(result.get_counts(superposition_state))


# Approximately half of the results are in the fundamental state and the other half in the excited state.

# ## Example 4
# 
# Two superpoistions

# Let's try now putting two H gates one after the other.

# In[20]:


# superposition_state_xbasis.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer


# In[21]:


# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)


# In[22]:


# Build the circuit
superposition_state_xbasis = QuantumCircuit(q, c)
superposition_state_xbasis.h(q)
superposition_state_xbasis.barrier()
superposition_state_xbasis.h(q)
superposition_state_xbasis.measure(q, c)


# In[23]:


# Draw the circuit
superposition_state_xbasis.draw()


# In[24]:


# Execute the circuit
job = execute(superposition_state_xbasis, backend = Aer.get_backend('qasm_simulator'), shots=1024)
result = job.result()


# In[25]:


# Print the result
print(result.get_counts(superposition_state_xbasis))


# ## Example 5
# 
# Negative superpoistion

# In[26]:


# negative_superposition_state.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer


# In[27]:


# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)


# In[28]:


# Build the circuit
negative_superposition_state = QuantumCircuit(q, c)
negative_superposition_state.x(q)
negative_superposition_state.h(q)
negative_superposition_state.measure(q, c)


# In[34]:


# Draw thecircuit
negative_superposition_state.draw()


# We first excite the q-bit with the X gate and then create a superposition using the H gate:
# 
# X gate creates a superposition between fundamental state and excited state in the same q-bit:
# 
# $ |-> = \frac{| 0 > - | 1 >}{\sqrt{2}} $ 

# In[32]:


# Execute the circuit
job = execute(negative_superposition_state, backend = Aer.get_backend('qasm_simulator'), shots=1024)
result = job.result()


# In[33]:


# Print the result
print(result.get_counts(negative_superposition_state))


# ## Example 6
# 
# Two negative superpoistions

# In[35]:


# negative_superposition_state_xbasis.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer


# In[36]:


# Define the Quantum and Classical Registers
q = QuantumRegister(1)
c = ClassicalRegister(1)


# In[37]:


# Build the circuit
negative_superposition_state_xbasis = QuantumCircuit(q, c)
negative_superposition_state_xbasis.x(q)
negative_superposition_state_xbasis.h(q)
negative_superposition_state_xbasis.barrier()
negative_superposition_state_xbasis.h(q)
negative_superposition_state_xbasis.measure(q, c)


# In[38]:


# Draw thecircuit
negative_superposition_state_xbasis.draw()


# In[39]:


# Execute the circuit
job = execute(negative_superposition_state_xbasis, backend = Aer.get_backend('qasm_simulator'), shots=1024)
result = job.result()


# In[40]:


# Print the result
print(result.get_counts(negative_superposition_state_xbasis))


# In[ ]:




