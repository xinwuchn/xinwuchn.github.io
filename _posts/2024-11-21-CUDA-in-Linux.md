---
layout: post
title: How to install CUDA in Linux?
date: 2024-11-21
description: The guidance is for installing CUDA within Linux system, and the further GPU computing.
tags: guidance
categories: Research
featured: false
thumbnail: assets/img/CUDA.png
toc:
  sidebar: false
giscus_comments: false
---

> Install the _NVIDIA Driver_ and _CUDA Toolkit_

> ##### TIP
>
> Traditionally, the _NVIDIA Driver_ and _CUDA Toolkit_ are installed separately,
> but you can actually install the _CUDA Toolkit_ directly, and the system will
> automatically install the _NVIDIA Driver_ that matches its version.
> {: .block-tip }

Following is the detailed installation steps, with CUDA-10.1 as an example:

###### **1. Check if there is a GPU that supports CUDA**

```shell
lspci | grep -i nvidia
```

###### **2. Install the _gcc_ and _make_**

```shell
sudo apt update
sudo apt install gcc g++ make
# Install the dependent libraries required to run the CUDA example
sudo apt install libglul-mesa libxi-dev libxmu-dev libglul-mesa-dev freelut3-dev
```

Sometimes, too high versions of _gcc_ and _g++_ may cause GPUMD compilation errors, so
you need to download lower versions of gcc and g++ and switch versions (gcc is used as a demonstration below):

- Check the current default _gcc_ version: `gcc --version`
- Check the installed _gcc_ version: `ls /usr/bin/gcc*`
- If there is no suitable version then required, perform a specified installation, such as: `sudo apt-get install gcc-7`
- Then perform manual version management: `sudo update-alternatives --config gcc`, that’s it.

###### **3. Download _CUDA Toolkit_**

[CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)

###### **4. Run and install**

The deb package can automatically install the _NVIDIA driver_ by default (the preferred way).

Note: when installing Ubuntu, press `E` to pop up GRUB mode, add `nouveau.modeset=0` at the end of the **Linux** line,
and then press `F10` to restart. Before installing Ubuntu dual system, please create a blank partition in advance.

> ##### WARNING: About Nouveau driver disabling
>
> Generally, the deb package to install CUDA will automatically install the _Nvidai driver_,
> but there may still be problems in actual testing. This may be caused by the open source driver Nouveau being incompletely disabled.
>
> - Open the balcklist: `sudo vim /etc/modprobe.d/blacklist.conf`
> - Insert the following content at the bottom and save it:
>
> ```text
> blacklist nouveau
> blacklist lbm-nouveau
> options nouveau modeset=0
> alias nouveau off
> alias lbm-nouveau off
> ```
>
> - Update: `sudo update-initramfs -u`
> - Check after restart: `lsmod | grep nouveau`
>   {: .block-warning }

###### **5. Modify environment variables**

```shell
sudo vim ~/.bashrc
```

Add the following environment variables:

```text
export PATH=$PATH:/usr/local/cuda-10.1/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.1/lib64
export CUDA_HOME=$CUDA_HOME:/usr/local/suda-10.1
```

###### **6. Test**

```shell
nvidia-smi
nvcc --version
```

nvcc is a CUDA C/C++ compiler that can directly compile source files (.cu) containing C++ syntax. The syntax is similar to gcc. Its path is located at `/usr/local/cuda-10.1/bin`
