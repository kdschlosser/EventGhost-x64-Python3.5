
# EventGhost


This is a test version of EventGhost. It is a work in progress.
This test version runs on Python 3.5 x64


## Build Requirement

These requirements are the needed ones to get the setup program running.
The rest of the requirements will be downloaded and placed into the .eggs
directory located in the same folder as the setup.py file. You can
delete this directory any time you like. If a module that meets the
requirements needed and is already installed on your system then that
is what will be used.

So you only need to install the 3 items listed below. Visual Studio is
a beast and if you do not have a need for the IDE then I would
recommend using the Visual C++ Build Tools you can download it from here

https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16


* Stackless Python x64 3.5.4: you can download it from here.
  http://www.stackless.com/binaries/MSI/3.5.4/stackless-3.5.4-amd64.exe

* MSVC version 10.0+: This can either be obtained by installing
  Visual Studio, Visual C or the Build Tools that may be available for
  either of those.

* Windows SDK: The version of your SDK is going to depend on which
  version of MSVC you are using. You will need to find out which SDK
  is supported by your compiler.


## Build Command

This is the only command you are going to need to use. It will compile
and package up EventGhost for you. the executable will be located in
the output folder in the same directory as the setup.py file.

    python setup.py build_exe

NOTE: make sure you run python from your stackless installation.


