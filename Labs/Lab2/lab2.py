# -*- coding: utf-8 -*-
"""lab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wUPyVex-dWk_trqfprX8S8jn_xum_YFk

<a href="https://colab.research.google.com/github/wingated/cs474_labs_f2019/blob/master/Alternate_Labs/DL_Lab2.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Lab 2: Intro to PyTorch

## Deliverable

For this lab, you will submit an IPython notebook via Learning Suite.
This lab will be mostly boilerplate code, but you will be required to implement a few extras.

**NOTE: you almost certainly will not understand most of what's going on in this lab!
That's ok - the point is just to get you going with PyTorch.
We'll be working on developing a deeper understanding of every part of this code
over the course of the next two weeks.**

A major goal of this lab is to help you become conversant in working through PyTorch
tutorials and documentation.
You should turn to the documentation first, but you may google whatever you need, as there are many great PyTorch tutorials online.

This notebook will have four parts:

* Part 1: Your notebook should contain the boilerplate code. See below.

* Part 2: Your notebook should contain a testing loop.

* Part 3: Your notebook should contain a visualization of test/training performance over time.

The resulting image could, for example, look like this:
![](http://liftothers.org/dokuwiki/lib/exe/fetch.php?cache=&w=900&h=608&tok=3092fe&media=cs501r_f2018:lab2.png)

* Part 4: Your notebook should contain the completed microtasks and pass all the asserts.

See the assigned readings for pointers to documentation on PyTorch.
___

### Grading standards:
Your notebook will be graded on the following:

* 40% Successfully followed lab video and typed in code
* 20% Modified code to include a test/train split
* 20% Modified code to include a visualization of train/test losses
* 10% Tidy and legible figures, including labeled axes where appropriate
* 10% Correct solutions to the microtasks
___

### Description
Throughout this class, we will be using PyTorch to implement our deep neural networks.
PyTorch is a deep learning framework that handles the low-level details of
GPU integration and automatic differentiation.

The goal of this lab is to help you become familiar with PyTorch.
The four parts of the lab are outlined above.

For part 1, you should watch the video below, and type in the code as it is explained to you.

A more detailed outline of Part 1 is below.

For part 2, you must add a validation (or testing) loop using the
FashionMNIST dataset with train=False

For part 3, you must plot the loss values.

For part 4, you must complete the microtasks and pass all asserts.

Optional: Demonstrate overfitting on the training data.

The easiest way to do this is to limit the size of your training dataset
so that it only returns a single batch (i.e. len(dataloader) == batch_size,
and train for multiple epochs. For example,
I set my batch size to 42, and augmented my dataloader to produce only 42
unique items by overwriting the len function to return 42.
In my training loop, I performed a validation every epoch which basically corresponded
to a validation every step.

In practice, you will normally compute your validation loss every n steps,
rather than at the end of every epoch. This is because some epochs can take hours,
or even days and you don’t often want to wait that long to see your results.

Testing your algorithm by using a single batch and training until overfitting
is a great way of making sure that your model and optimizer are working the way they should!

___

### Part 0
Watch Tutorial Video

[https://youtu.be/E76hLX9WCLE](https://youtu.be/E76hLX9WCLE)

**TODO:**
* Watch video

**DONE:**

Watched video

___

### Part 1
Your notebook should contain the boilerplate code. See below.

**TODO:**

* Replicate boilerplate from the video

**DONE:**

Replicated boilerplate from the video

___

### Part 2
Your notebook should contain a testing (validation) loop.

**TODO:**

* Add a testing (validation) loop

**DONE:**

Added a testing validation loop
"""

!pip3 install torch
!pip3 install torchvision
!pip3 install tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms, utils, datasets
from tqdm import tqdm

assert torch.cuda.is_available() # You need to request a GPU from Runtime > Change Runtime Type

# Write the boilerplate code from the video here
class LinearNetwork(nn.Module):
  def __init__(self, dataset):
    super(LinearNetwork, self).__init__()
    x, y = dataset[0]
    c, h, w = x.size()
    out_dim = 10

    self.net = nn.Sequential(nn.Linear(c * h * w, 1000),
                             nn.ReLU(),
                             nn.Linear(1000, out_dim))
  def forward(self, x):
      n, c, h, w = x.size()
      flattened = x.view(n, c*h*w)
      return self.net(flattened)

# Create a dataset class that extends the torch.utils.data Dataset class here
class FashionMNISTProcessedDataset(Dataset):
  def __init__(self, root,train=True):
    self.data = datasets.FashionMNIST(root, train=train,
                                      transform=transforms.ToTensor(),
                                      download=True)
  def __getitem__(self,i):
    x, y = self.data[i]
    return x, y

  def __len__(self):
    return len(self.data)

# Extend the torch.Module class to create your own neural network

# Instantiate the train and validation sets
train_dataset = FashionMNISTProcessedDataset('/tmp/fashionmnist', train=True)
val_dataset = FashionMNISTProcessedDataset('/tmp/fashionmnist', train = False)

# Instantiate your data loaders
model = LinearNetwork(train_dataset)
model = model.cuda()
train_loader = DataLoader(train_dataset, batch_size = 42, pin_memory=True)
Validation_loader = DataLoader(val_dataset, batch_size=42)

# Instantiate your model and loss and optimizer functions
optimizer = optim.SGD(model.parameters(), lr=1e-4)
objective = torch.nn.CrossEntropyLoss()

train_losses = []
validation_losses = []
cntr = 0

num_epochs = 10

loop = tqdm(total=len(train_loader) * num_epochs, position=0)

# Run your training / validation loops
for epoch in range(num_epochs):
  batch = 0
  for x, y_truth in train_loader:
    x, y_truth = x.cuda(non_blocking=True), y_truth.cuda(non_blocking=True)

    optimizer.zero_grad()

    y_hat = model(x)
    loss = objective(y_hat, y_truth)

    if epoch % 2 == 0 and batch == 0:
      train_losses.append(loss.item())
      validation_loss_list = []
      for val_x, val_y_truth in Validation_loader:
        val_x, val_y_truth = val_x.cuda(non_blocking=True), val_y_truth.cuda(non_blocking=True)
        val_y_hat = model(val_x)
        validation_loss_list.append(objective(val_y_hat, val_y_truth).cpu())
      validation_losses.append(sum(validation_loss_list).item()/float(len(validation_loss_list)))


      cntr += 1
    loop.set_description('batch:{} loss:{:.4f} val_loss:{:.4f}'.format(batch, loss.item(), validation_losses[-1]))

    loss.backward()
    optimizer.step()
    batch += 1
loop.close()

"""
___

### Part 3
Your notebook should contain a visualization of test/training
performance over time. Use matplotlib.pyplot, and label the graph's axes.

**TODO:**
* Add a visualization of test/train performance (i.e. loss) over time.

**DONE:**
"""

# Write your code to create a plot of your loss over time
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range(len(validation_losses)), validation_losses, label = 'Validation Loss')
ax.plot(range(len(train_losses)), train_losses, label='Training loss')
plt.xlabel('Epoch')
plt.ylabel('Cross Entropy Loss')
plt.title('Training and Test Performance')
plt.show()

"""___

### Part 4
Complete the following microtasks to learn some important PyTorch skills.

If you do not know how to complete one of the microtasks, use [PyTorch's documentation](https://pytorch.org/docs/stable/index.html)! PyTorch is very well documented, and you will need to learn how to use the documentation, especially in later labs.

**TODO:**
* Complete microtasks

**DONE:**

completed microtasks

### Computation Graph Microtasks
"""

# To understand how PyTorch organizes the computation graph, let's walk through
# a quick example!

# 1. First, construct a tensor 'a' that contains 10 random floats.
# This will simulate the output layer of a network. Hint: use `torch.rand`.
a = torch.rand(10)
print(a)
assert a.size() == torch.Size([10])

# 2. Now turn 'a' into an `nn.Parameter` so that it be attached to the computation
# graph.
a = nn.Parameter(a)
print(a)
assert type(a) == nn.Parameter

# Notice that our original tensor 'a' is nested inside of a Parameter object.
# The Parameter object knows that it will need to compute gradients at some point.

# No need to do anything here, but this assert should pass.
assert a.requires_grad == True

# 3. Let's run 'a' through a loss function. The output of the loss function is
# just another tensor, but this tensor remembers what operations produced it.
loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(a.unsqueeze(0), torch.Tensor([7]).long())
print(loss)

# Now, instruct the network to do a backward pass, by calling '.backward()' on the
# result of the loss function. We should now be able to see the gradients that
# were computed for 'a' w.r.t. the loss.
loss.backward()
assert a.grad is not None
print(a.grad)

# 4. If we were to use 'a' in another operation, this might affect the computation graph.
# To make sure that you are not adversly affecting the computation graph, call
# `.detach()` on 'a' and assign the result to a new variable 'b'.

b = torch.detach(a)

print(a)
print(b)
assert a.requires_grad == True
assert b.requires_grad == False