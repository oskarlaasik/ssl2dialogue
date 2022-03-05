# ssl2dialogue

This project parses dialogue from fallout 1 & fallout 2. 

### You need to unpack the data file:
 
The .dat files are located in the game's main directory.

https://github.com/falltergeist/dat-unpacker
 
or use a similar tool.

#### decompile the int file

you can use convert int2ssl script to do so. You need to install int2ssl decompiler before running the script. 

https://github.com/falltergeist/int2ssl

Then run:
```console
 ./int2ssl.sh pathToUnpackedDatDir/SCRIPTS
```

Run the dialogue unpacker with:
```console
python parse_ssl.py  -l datFiles/F1 -l datFiles/F2
```

tested with python 3.7



