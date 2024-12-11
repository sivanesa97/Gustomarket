## For GustoMarket setup

## Required python version
Python 3.8.10 and above

## for setup virtual environment and Django Setup
# ubuntu
 $ mkdir Gusto
 $ cd Gusto
 Gusto$ python3 -m virtualenv myenv
 Gusto$ source myenv/bin/activate

 Gusto$ cd GustoMarket/

 Gusto/GustoMarket$ pip install -r requirements.txt
 Gusto/GustoMarket$ python3 manage.py makemigrations
 Gusto/GustoMarket$ python3 manage.py migrate
 Gusto/GustoMarket$ python3 manage.py createsuperuser
 Gusto/GustoMarket$ python3 manage.py runserver
