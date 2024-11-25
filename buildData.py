# -*- coding: utf-8 -*-

"""
« Copyright © 2024, Philippe Gambette
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders X be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.

Except as contained in this notice, the name of the <copyright holders> shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from the <copyright holders>. »
"""
import csv, glob, os, re, sys

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

# Prepare the output HTML file
outputFile = open("dataElections.csv", "w", encoding="utf-8")
outputFileDep = open("dataElectionsDep.csv", "w", encoding="utf-8")
outputFileDep.writelines("source,dep,inscrits,votants,exprimes\n")

# Open the input files
# All CSV files extracted from the ZIP files downloaded from https://unehistoireduconflitpolitique.fr/telecharger.html should be placed in the `data` folder.
for file in glob.glob(os.path.join(folder, os.path.join("data", '*.csv'))):
   print("Treating file " + file)
   inputFile = open(file, "r", encoding="utf-8")
   lineNb = 0
   dep = ""
   inscrits = 0
   votants = 0
   exprimes = 0
   # For each line of the CSV file
   for line in inputFile:
      # Ignore the first line containing headers
      if lineNb > 1:
         # Extract some of the values about the "département" code as well as the number of voters (with 3 criteria)
         res = re.search("^(([^,]*),[^,]*,[^,]*,[^,]*,([^,]*),([^,]*),([^,]*)),", line)
         if res:
            #print(res.group(1))
            outputFile.writelines(res.group(1) + "\n")            
            if res.group(2) != dep:
               # A new "département" was found, add the total numbers of voters to the output file
               if dep != "":
                  # Extract the year of the election from the file name
                  outputFileDep.writelines(os.path.basename(file).replace("comm.csv","") + "," + dep + "," + str(inscrits) + "," + str(votants) + "," + str(exprimes) + "\n")
               dep = res.group(2)
               inscrits = 0
               votants = 0
               exprimes = 0
            nbExprimes = res.group(5)
            nbInscrits = res.group(3)
            # Check if the number of voters is well defined (it should neither be empty nor negative)
            if nbExprimes=="" or float(nbExprimes) < 0:
               nbExprimes = "0"
            if int(round(float("0"+nbExprimes),0)) > int(round(float("0"+res.group(3)),0)):
               nbInscrits = 0
            else:
               nbInscrits = int(round(float("0"+res.group(3)),0))
            # Add the number of voters to the total by "département"
            inscrits += nbInscrits
            votants += int(round(float("0"+res.group(4)),0))
            exprimes += int(round(float("0"+nbExprimes),0))
                  
      lineNb += 1
   # Add the total numbers of voters of the last "département" to the output file
   outputFileDep.writelines(os.path.basename(file).replace("comm.csv","") + "," + dep + "," + str(inscrits) + "," + str(votants) + "," + str(exprimes) + "\n")

outputFile.close()
outputFileDep.close()
print("Fini !")