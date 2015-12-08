Sendmail 
------

This is a small automation console script. It is written to automate small mailing list from generated CSV file.

**Note**: it was tested only on Linux. To launch it on Windows, at least you will need to change input redirect commands.


###Usage

* configure email server
* prepare input data
* write a template
* test rendering
* send emails

### Configure email server

Open `settings.py`. Set `smtp_server`, `use_tls`, `use_ssl`, `username` and `password`. If you have ready template, you can adjust `template_path` or `template` as well.


###Prepare input data

Script accepts CSV content from standard input. First line of CSV is treated as column names. Column *email* should present and will be used a recipient address. Other columns will be used for template rendering. Example of CSV content:

    name,date,balance,email
    John Doe,12/31/2015,0.23,johndoe@email.com
    ...

**Note**: This script works with CSV files, which means *comma* separated values. MS Office uses semicolon (;) separator by default. If you use MSO, change separator to comma when saving the CSV.

###Write a template

File `template.txt` contains email body template. Put variables corresponding to your CSV columns in curly braces. Example of template for rendering the CSV above:

    Dear {name},
    
    We would like to inform you that as of {date} your account 
    balance is {balance}.
    
    Sincerely,
    your support team X.

###Test rendering

To do a dry run, run without `-y` key:

    ./sendmail.py "Put email subject here" < test.csv

You will get something like:

    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit
    Subject: Put email subject here
    from: 
    To: johndoe@email.com
    
    Dear John Doe,
    
    We would like to inform you that as of 12/31/2015 your account
    balance is $0.23.
    
    Sincerely,
    your support team X.
    
    ================================================================================
    This is an example of emails that would be sent.
    If you want to really send them, add -y to the command.
    ================================================================================

**Note**: As you might have a long list of recipients, it makes sense to test output on a small subset of them. You can also use pass result to `more`, `less`, `head` or `tail`:

    ./sendmail.py "Put email subject here" < test.csv | tail

###Send emails

Finally, when you have everything in place, add `-y` to the command:
Example usage:

    ./sendmail.py -y "Put email subject here" < test.csv

    
###License

Licensed under MIT license