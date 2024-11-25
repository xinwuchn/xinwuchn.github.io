---
layout: post
title: Run CMD on Win system without entering it
date: 2024-11-22
description: What to do if you forget your login PIN code in Windows system？
tags: guidance
categories: Research
featured: false
thumbnail: assets/img/WinPin.png
toc:
  sidebar: false
giscus_comments: false
---

> Applicable scenarios: There is a problem with the computer PIN code, your PIN is not available,
> click to reset: `msconfig` after diagnostic startup.

1. In the login page, hold on `shift` and click `Restart` in the lower right corner: automatically enter the PE recovery environment.
2. Troubleshooting -> Advanced Options -> Command Prompt
3. Enter the following two lines of commands one by one:

```shell
move c:\windows\system32\utilman.exe c:\
copy c:\windows\system32\cmd.exe c:\windows\system32\utilman.exe
```

4. Close the command prompt window, and after restarting, click the "Easy to Use" button (little person) in the lower right corner to call the command prompt.
   > If you want to solve the problem that the PIN code cannot be used because the startup item fails to load the PIN function, do the following:
5. Enter `msconfig` and press `Enter` to open the system configuration window. Change the startup selection to "normal startup" or "selective startup", restart, and then enter the PIN normally to enter the system.
6. Finally, move the file utilman.exe in the root directory of drive C to the directory `C:\Windows\System32\`, and replace the file after granting administrator rights. (The following step is for that "Easy to Use" will become CMD or not.)
