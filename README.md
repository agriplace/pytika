# PyTika

![Workflow status](https://github.com/agriplace/pytika/actions/workflows/main.yml/badge.svg)
![PyPi wheel](https://img.shields.io/pypi/wheel/pytika)

An Apache Tika Server python client.

## Installation

You can install the package simply from pypi:
```pip install pytika```


## Usage
This package is a python client for Apache Tika Server, so you'll need to have Tika Server running locally somehow.
I would recommend using the docker image as that's the simplest.
```docker run --name tika-server -it -d -p 9998:9998 apache/tika:2.7.0-full```

After you have that running, you can use PyTika to interface with it.

### Metadata queries
```python
from pytika.api import TikaApi

tika = TikaApi()
metadata = api.get_meta(file)

"""
>>> metadata
{
    'Content-Type': 'application/pdf',
    ...
}
"""
```

### Text detection queries

For text detection, Tika Server usually decides on the response type (typically xml/html is the default).
To force it to return plain text (Accept: text/plain header) you can set the following configuration:

```python
from pytika.api import TikaApi
from pytika.config import GetTextOptionsBuilder as opt

tika = TikaApi()

with open("yourfile.whatever", "rb") as file:
    text = api.get_text(file, opt.AsPlainText()).decode()

```

Notice the awkward configuration - passing a function call as an option - this is coming from a nice Golang standard that makes calling complex APIs a little friendlier. Since we have a lot of options, instead of having each be an argument, we can define an "option class" with chainable functions. This allows the API to validate each separately, avoid having a massive list of arguments for get_text, as well as tidy up the API code. (For more info: [Uptrace](https://uptrace.dev/blog/golang-functional-options.html), [Dave Cheney's post](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis))


For detection in HOCR format with bounding boxes:

```python
from pytika.api import TikaApi
from pytika.config import GetTextOptionsBuilder as opt

tika = TikaApi()

with open("yourfile.whatever", "rb") as file:
    text = api.get_text(file, opt.WithBoundingBoxes()).decode()

```


There are many more configuration options that you can look into in the GetTextOptionsBuilder class, and more to come in the future.



## Contribution Guide

If you'd like to add some missing features that you can find in TikaServer or Tika, then you can contribute to this repo yourself!

1- Clone the repository
```
git clone "url from repo, either ssh or https"
```

2- Create a branch
```
cd pytika
git switch -c your-new-branch-name
```

3- Make necessary changes and commit, and push to Github
```
git add README.md
git commit -m "Updated README.md with new API changes"
git push -u origin your-new-branch-name
```

4- Go to your repository and you'll see a `Compare and pull request` button, click on that.

5- Wait for us to review your PR, likely leave comments, and hopefully merge it in!

