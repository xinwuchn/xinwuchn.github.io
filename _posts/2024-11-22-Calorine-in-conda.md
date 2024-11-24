---
layout: post
title: Install calorine on conda-MacOS
date: 2024-11-22
description: If you have problems installing calorine on MacOS, please see here.
tags: guidance
categories: Research
featured: false
thumbnail: assets/img/calorinelogo.png
toc:
  sidebar: false
giscus_comments: false
---

> MacOS14.5 + Python 3.10 + conda: The error always shows that it is a problem with C++ compilation, which may be related to the c++ compiler of the MacOS system.

> ##### The errors one may encounter
>
> Error 1:
>
> ```text
> File "<string>", line 69, in build_extensions
> File "<string>", line 46, in cpp_flag
> RuntimeError: Unsupported compiler -- at least C++11 support is needed!
> [end of output]
> ```
>
> Error 2:
>
> ```text
> clang-14: error: invalid argument '-bundle' not allowed with '-dynamiclib'
> error: command '/opt/homebrew/opt/llvm@14/bin/clang++' failed with exit code 1
> [end of output]
> ```
>
> {: .block-warning }

Follow the steps:

###### **1. Modify _setup.py_ in calorine package**

Download the [source code](https://gitlab.com/materials-modeling/calorine) from Gitlab and comment out the following content in setup.py:

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/calorine_error.png" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

###### **2. Make sure to use _clang_ and _gcc_ from Xcode.app**

- Put the system's /usr/bin path at the front of the PATH variable so that the system's clang will be found first:

```shell
export PATH="/usr/bin:$PATH"
```

- Explicitly set the CC and CXX environment variables to the system's clang and clang++:

```shell
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
```

- Verify the above settings:

```shell
which clang
/usr/bin/clang
which clang++
/usr/bin/clang++
```

- If you want these settings to be automatically applied every time this conda environment is activated, you can add the above command to the conda environment's activation script. Assuming your conda environment is named For_Research: Create or edit the file ~/opt/anaconda3/envs/For_Research/etc/conda/activate.d/env_vars.sh (you can create these directories manually if the path does not exist):

```shell
mkdir -p ~/opt/anaconda3/envs/For_Research/etc/conda/activate.d
nano ~/opt/anaconda3/envs/For_Research/etc/conda/activate.d/env_vars.sh
# After opening it with nano, add the following content:
#!/bin/bash
export PATH="/usr/bin:$PATH"
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
```

- After saving and closing the file, make sure the script has executable permissions:

```shell
chmod +x ~/opt/anaconda3/envs/For_Research/etc/conda/activate.d/env_vars.sh
```

- Reactivate your conda environment to apply these changes:

```shell
conda deactivate
conda activate For_Research
which clang
which clang++
```

- If the above steps are correct, you should see your system's clang path.

###### **3. Compile**

Finally, in the calorine path of the source code, please compile it:

```shell
pip install .
```

Well done!!! 🎉

```text
Successfully installed calorine-2.3 numpy-1.26.4
```
