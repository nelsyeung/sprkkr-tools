# SPRKKR Tools

## Installation
```
git clone https://github.com/nelsyeung/sprkkr-tools.git
```

## Usage
Make sure you are inside the sprkkr-tools directory.
```
cd sprkkr-tools
```
Move one of the example scripts inside the examples directory into the root
directory.
```
mv examples/kkrtools.inp .
```
Edit the input file to your needs and execute the generate script.
```
./generate
```
A generated folder should be created with the newly generated systems.  
You may now submit the pbs script inside the generated/$system folder.
```
cd generated/MgZnSiSnBi
qsub pbs.pbs
```

## Available options
Check the kkrtools.default file inside the templates directory for the list of
available options with their defaults.
