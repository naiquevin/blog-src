Title: Windows 7-Ubuntu dual boot without using wubi
Author: Vineet Naik
Date: 2010-06-12 23:29:03
Tags: Ubuntu, disk, partition, wubi, Linux
Category: ubuntu
Summary: Step by step guide to setting up Windows7-Ubuntu dual boot
Status: published


Last week I finally managed to set up a windows 7 - Ubuntu dual boot
system on my home computer after spending substantial amount of time
on the [ubuntuforums](http://ubuntuforums.org). So i thought, why not
note down the process while all the new concepts, problems and
workarounds are fresh in the mind. And what would be a better way to
do this than writing a blog post. I am sure this guide will help any
one looking to set up a windows-ubuntu dual boot.<!--more-->

Before I start, let me be very clear that I am not a Ubuntu expert let
alone a Linux expert. But I won't call myself a beginner either. I
have been using Jaunty Jackalope (9.04) at work for some 3-4 months
and am very comfortable at it. The only problem I have is that, well,
its wubi installed.

**Why is 'wubi-installed' a problem?**

[wubi](http://wubi-installer.org/) is the name of the installer that
comes with the ubuntu iso. It installs ubuntu on windows (and can
later uninstall it) just like any other program and thus saving us the
effort of formatting and partitioning of disks. And its very very
easy, infact it can't get any more easier than this. But there are
problems. My limited knowledge allows me to have only two of them.

1. The maximum memory available for use in wubi installed ubuntu is
   30gb which i feel is very less. Only 3 months and its already reduced
   to just 10gb.

2. I am not able to figure out if and how i can recover data stored
   under ubuntu if any thing goes wrong. Thankfully, all the code is safe
   with svn in place.

So, in order to fight these two problems, i was really looking forward
to doing a live cd installation with partitioning of disks and
everything as soon as I get my hard disk upgraded so that I could do
it in office with some experience.

Okay, so lets get started.

**Requirements-**

1. Ubuntu 10.04 iso downloaded from [here](http://www.ubuntu.com/desktop/get-ubuntu/download).
2. An already running windows OS.
3. A decently fast internet connection.
4. All data backed up if at all anything goes wrong at any stage.
5. A blank cd to write the iso to.


**Step 1: The ubuntu image file.**

The ubuntu image file is an iso file which can either be burnt into a
cd or can be extracted using
[winrar](http://www.rarlab.com/download.htm). The later method is
recommended if you want to do a wubi installation. If you are trying
Ubuntu for the first time there is absolutely no harm in going for the
wubi installation. In fact it will help you familiarize yourself with
Linux OS and decide if you want to switch to it full time. In case you
do, just make sure you don't keep using wubi the way I did.

We are interested in the first method, so burn the image into a
CD. With the live CD, we can still try Ubuntu without installation
which is what we are going to do now.

Insert the CD into your CD-ROM and restart the machine. Make sure
'boot from CD/DVD' option is selected in the BIOS as priority so that
the system starts Ubuntu instead of loading windows. Now I don't
know how to explain this without a screen-shot but when you see a
purple background with two weird icons (one that looks like vitruvian
man and the other like a window or may be a keyboard) at the bottom,
press any key. It will now show a menu and the good old memories of
doom and quake will come to your mind.  Select the option 'Try Ubuntu
without installation'. At this stage you may want to go ahead with the
installation if partitioning is done. But I would strongly advise
against it as it showed me some error. The install option is available
later as well.


**Step 2: Connecting to the INTERNET**

Running Ubuntu w/o installation is also an opportunity of preparing
for the installation. An important part of that is connecting to the
Internet. Actually, it is not absolutely necessary but only if you
don't mind the Linux clock a few hours ahead of (or behind) your
windows clock. Trust me its really annoying. Good news is that there
is a way to fix that too. The second reason for this is that it gives
you something to do while the system installs itself.


**Step 3: Partition the disks.**

Yes we will be using Linux for partitioning. But before that its time
to understand some partitioning basics.  In windows we have our hard
disk organized in more than one drives which have alphabetical names
like C,D,E etc. In Linux however the naming convention is
different. The drives C,D,E in windows will be called something like
sda1, sda2, sda3 etc. To check this, open up the terminal and type,

```bash
    $ sudo fdisk -l
```

With some knowledge about the space in each drive and a little guess
work, it is quite easy to map the drives in these two systems.

Now I am assuming that you already have windows running where all
available hard disk memory has been allocated to different drives. In
this case we need to free up some memory for Ubuntu. That is by
shrinking the drives. I prefer to do this in windows. So restart your
machine after ejecting the Ubuntu CD allowing windows to load this
time.  Inside windows 7, click on start and search for 'Computer
Management'. When the window opens, go to Storage > Disk Management
and all the disks will appear there. Right click on the disk you don't
mind shrinking, and say shrink volume. Then simply follow the
instructions. When shrinking is complete you will see some part of
memory shown as 'Unallocated'. This is where Ubuntu will reside.

For installing Ubuntu, we will need 3 partitions. We will get to that
in a bit. For now, lets continue with some more partitioning concepts.


**Primary, Extended and Logical Partitions** 

Any hard drive can have a maximum of 4 primary partitions. But more
partitions are possible by defining one of the partitions as
'Extended' and then partitioning it further into any number of
'Logical' partitions. More info
[here](http://www.pcguide.com/ref/hdd/file/structPartitions-c.html).

With this much knowledge we go back to Ubuntu and again say, '*try
without installation*' when prompted and connect to the Internet. Now
start [GParted](http://gparted.sourceforge.net/) (or Disk Utility)
from system > administration and create 3 partitions. First create a
primary partition of the entire unallocated space and mark it as
'Extended'. Then divide this into 3 logical partitions as follows,

Say we have 150 GB for Ubuntu in total

* 1st partition will be around 20gb. choose the
  [EXT Journaling file system](http://en.wikipedia.org/wiki/Ext3). I
  selected EXT3.
* 2nd partition will be around twice the size of your RAM. I selected
  8gb. This will be used as *swap space* which will kind of support
  the RAM if required when running multiple applications on
  Ubuntu. Under files system, choose '*Linux swap*' option for this.
* Now allocate all the remaining space to the 3rd partition which will
  also be a logical partition and EXT3.


**Why do we need 3 partitions?**

Lets call the above partitions A, B, C for understanding
convenience. During installation we will select such a configuration
that Ubuntu is installed on A and we have the bigger C for storage
while B will be used as swap. This will make sure the data is safe if
we need to reinstall or upgrade Ubuntu at any time.


**Step 4: Proceeding with installation**

With this much knowledge we can start the installation. Click on the
'install Ubuntu' icon on desktop.

I don't think detailed procedure is required after this as it is a
very straight forward process. Just keep following the instructions
until you reach the disk partitioning stage.

Here select '*manually partition disks*'. In the next screen, you can
see the three partitions we just created along with the windows
partitions. Now is the moment we tell the installer where to install
what by specifying the mount point for each disk. For our disk A
above, we select '/' (root) as the mount point and for the disk C we
select '/home'. The mount point field for swap area will be rightly
disabled.

Then proceed to follow some more instructions until it the actual
coying of files and installation starts. Open up Firefox to surf the
Internet or just sit back and relax. After the installation is
complete restart the machine and the system will prompt you to choose
the OS to load at boot. Congrats you just installed Ubuntu aside
windows 7.

I hope this helped. Now you might want to read my
[post](http://www.kodeplay.com/2010/04/windows-to-linux-transition/)
on my company's [blog](http://www.kodeplay.com/blog) about setting up
PHP development environment on Ubuntu and a few other tricks.
