Sendmail 
------

This is a small automation console script. It is written to automate small mailing list from generated CSV file.

###Usage

Example usage:

    ./sendmail.py -y "Put email subject here" < test.csv

To do a dry run, run without `-y` key:

    ./sendmail.py "Put email subject here" < test.csv
    
It will output generated emails to console so you can check them. If it is a long list, probably passing it to `less` would be a good idea:

    ./sendmail.py "Put email subject here" < test.csv | less

###Input data

Script accepts CSV file on standard input. First line of CSV is treated as column name. Column email should contain email address of recipient. Other columns will be used for template formatting. Example of CSV content:

    name,date,balance,email
    John Doe,12/31/2015,0.23,johndoe@email.com
    ...
    
Besides CSV, you also need to pass email subject as first parameter to the script.

    ./sendmail.py "EMAIL SUBJECT HERE" < test.csv


###Template formatting

File `template.txt` contains email body template. In curly braces you can put variables corresponding to columns in your CSV. Example of template for rendering the CSV above:

    Dear {name},
    
    We would like to inform you that as of {date} your account 
    balance is {balance}.
    
    Sincerely,
    your support team X.
    
###License

Licensed under MIT license