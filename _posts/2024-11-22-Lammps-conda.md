---
layout: post
title: Install lammps in conda environment
date: 2024-11-22
description: Do some simple lammps test in conda environment.
tags: guidance
categories: Research
featured: false
thumbnail: assets/img/Lammpsconda.png
toc:
  sidebar: true
giscus_comments: false
---

###### **1. Create a new conda environment and enter**

```shell
conda create --name YOUR_NAME python=3
conda activate YOUR_NAME
```

###### **2. Install lammps package using pip**

```shell
pip install lammps
```
Note that you must ensure that the pip package exists in the conda environment itself, which can be viewed through `conda list`.

###### **3. Test your installation**

Prepare a simple lammps in.lj file:
```text
# LAMMPS input script - in.lj
  
# Initialization
clear
units lj
dimension 3
atom_style atomic
  
# Atom definition
lattice fcc 1.0
region box block 0 10 0 10 0 10 units lattice
create_box 1 box
create_atoms 1 box
mass 1 1.0
    
# Potential
pair_style lj/cut 2.5
pair_coeff 1 1 1.0 1.0 2.5
    
# Run
run 1000
```

###### **4. Execute the above in.lj file in python script**

```python
from lammps import lammps
lmp = lammps()
lmp.file("in.lj")
```

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/condalammps.png" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    If you get this result, congratulations! 🎉 🎉 🎉.
</div>



###### **5. Exit the test environment**

```shell
conda deactivate
```
