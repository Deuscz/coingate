# coingateimpl


## Getting Started

Firstly you need to register on [https://coingate.com/](https://coingate.com/). 

Then you need to create new App and get Token.


### Installing


Download or clone project:

```
git clone https://github.com/Deuscz/coingateimpl.git
```

### Setting up


Set your token at views.py
```
auth_token = ''  # set your token
```


If you want to use this app not in sandbox environment you need to update all links in views.py

#### For example:
from 

```
url = 'https://api-sandbox.coingate.com/v2/orders'     #   
```

to

```
url = 'https://api.coingate.com/v2/orders'     #   
```
<<<<<<< HEAD
=======

>>>>>>> 8e47d441733eb1161666a9e48425de6bb5e92bfc
