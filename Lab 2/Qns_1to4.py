#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np

arr = np.arange(1, 11)  
print(arr)
print("Mean:", arr.mean())
print("Max:", arr.max())
print("Min:", arr.min())


# In[4]:


arr = np.array([10, 20, 30, 40, 50])

print("Third element:", arr[2])
print("First three elements:", arr[:3])

arr[2] = 35
print("After replacing 30 with 35:", arr)


# In[5]:


arr = np.arange(1, 10).reshape(3, 3)
print(arr)

print("Shape:", arr.shape)
print("Sum of all elements:", arr.sum())
print("Sum of each row:", arr.sum(axis=1))


# In[12]:


arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])
print(arr[1, 1])
print(arr[:, -1])
print(arr[1, :])


# In[ ]:




