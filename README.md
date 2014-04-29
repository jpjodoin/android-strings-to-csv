android-strings-to-csv
======================



Simple python 2.7 script to convert multiple android strings.xml files to a CSV and back to XML. Allows easy translation via Excel or similar. 

##Converting multiple strings.xml to CSV:
We assume a regular Android project structure 

projectroot/res/values/
projectroot/res/values-fr/
projectroot/res/values-es/
...
etc. 

Use androidproject2csv.py and follow the prompts.

##Converting CSV to multiple strings.xml:
Once your translations are done (each new translation should be a new column), run csv2androidproject.py and follow the prompts to create the XML file back.


##Notes:
Tab (\t) are used as a separator for the CSV, so take that into account when importing in your favourite spreadsheet software. Avoid writing tab in your strings. You can easily change it in both script if you'd prefer to use another
separator.




