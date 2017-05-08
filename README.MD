# Hamilton Lottery Automator

A script to go to the SF Hamilton Lottery website and fill out an application for lottery tickets.

## Setup
1. Create a secrets.sh file with your variables. It should look something like this:
```
export FNAME="Jane"
export LNAME="Smith"
export EMAIL="example@example.com
export ZIPCODE="12345"
export AGE=25
export NUMTICKETS=2 # optional
export PHONE="5551234567" # optional
export CHROME_DRIVER="/path/to/.virtualenvs/hammy/bin/chromedriver"
```

2. Install `requirements.txt`

3. Install the chrome driver and make sure `CHROME_DRIVER` in your `secrets.sh` file points to where
install the chrome driver.

You should now be able to run `sh auto_lottery.sh` and it should work fine. Remove the `-d` when
running `auto_lottery.sh`. Note that this will run in debug mode and won't submit the form.

## To Run on AWS Lambda
1. Install the _*linux*_ version of phantomjs and place the phantomjs binary in the root of this
project.
1. Run `sh mklambda.sh`. This will copy all the dependencies and the auto_lottery.py file into a
zip file that you can upload straight to AWS lambda. Make sure `mklambda.sh` is pointing to all the
right places for your dependencies.
1. If the script is timing out, increase the timeout on the lambda function.
1. Set a trigger for the lambda function with the CloudWatch Events Schedule so that it will run
every day at 11:17 am every day except for Monday (since there are no shows on Mondays):
```
 cron(17 11 ? * 1,3-7 *)
```