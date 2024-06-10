## Setting up OpneCV

### Ill be installing conda or anaconda on this Jetson nano and will be installin openCV in it.
**How to Setup a Jetson Nano for AI Projects in 2021**

Source: https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/
Jetson Nanos were released in 2019 and they are still not as popular as the Raspberry Pi-s. I own both of these units and Jetson Nano is not as straight forward to setup. In fact, it took me quite a while to figure it out and so I decided to write this up to save you guys from the hassle. This article aims to share an updated version on how to setup a Jetson Nano to run Tensorflow and PyTorch with “Anaconda” installed.

Step 1: The easy part…
Go to https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit and follow the instructions to download the image and set it up into the SD card. This part is so straight forward that I am not going to cover.

After you plug in the SD card into the Jetson Nano and you booted the machine up for the first time. You should follow the on screen instructions to setup an account and setup the name of your device etc. Now when you download the Dev Kit, please take note of the version you are downloading:

jetson-nano-jp46-sd-card-image.zip // my version
jetson-nano-jp<version_no>-sd-card-image.zip 
You need to check your version number. Mine is 46 but who knows whether they will release a new version.

Now open up the terminal and please run the following codes to do some updating and upgrading:

```
$ sudo apt update
$ sudo apt upgrade
```

Then you also need to install some important python packages:
```
$ sudo apt install python3-h5py libhdf5-serial-dev hdf5-tools python3-matplotlib python3-pip libopenblas-base libopenmpi-dev
```
Now your system is ready for installing “anaconda”.

Step 2: Installing “Anaconda”
Now this is a bit tricky because one thing you must understand is that Jetson Nano’s linux system runs in AArch64 architecture so installing the regular Anaconda does not work! So you have two options: to install Archiconda or Miniforge instead. In this tutorial, I will be using Archiconda. Run the following codes to download and install it.
```
$ wget https://github.com/Archiconda/build-tools/releases/download/0.2.3/Archiconda3-0.2.3-Linux-aarch64.sh
$ sudo sh Archiconda3-0.2.3-Linux-aarch64.sh
```
Now you should create an Python 3.6 (Yes! It must be python 3.6!) environment like a regular device with Anaconda installed:
```
$ conda env create -n torch python=3.6
```
[warning]
> here i faced error in Jetson nano specifically, because jetson was not giving write permission to the archiconda, so i had to give write permission to the whole archiconda installed : 
> ```sudo chown 1000:1000 /home/gecetc/archiconda3/*```
> Now run the command again to create the environment.

Next, we will be installing torch in this environment.

Step 3: Installing Tensorflow and PyTorch
Now you need to install PyTorch from Nvidia:

$ wget https://nvidia.box.com/shared/static/9eptse6jyly1ggt9axbja2yrmj6pbarc.whl -O torch-1.9.0-cp36-cp36m-linux_aarch64.whl
$ pip install torch-1.9.0-cp36-cp36m-linux_aarch64.whl
And after you create another environment, you can install Tensorflow with:

$ sudo pip install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 tensorflow
At last, you need to use nano (or whatever text editor you prefer) to adjust ~/.bashrc

$ nano ~/.bashrc
to add this at the bottom of the file:

export OPENBLAS_CORETYPE=ARMV8
Done!
Now you can launch and host your projects. What I did is that I used the Jetson Nano to host my Twitter Sentiment Bot for AAPL @AAPLinsights. Essentially it computes various sentiment scores related to AAPL. If you are into algorithmic trading or sentiment analysis with deep learning. Please feel free to follow this project -> https://twitter.com/AAPLinsights !


