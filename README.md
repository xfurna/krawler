# Krawler
A web crawling agent implemented to browse the seed in _breath first search_ fashion; while skipping over the selected, negligible domains & subdomains.

## Installation

### Install dependencies
```
$ pip3 install pipenv
$ pipenv install
```

### Activate the virtual environment
```
$ pipenv shell
```

## Usage
Edit `params.py` to set your seed and negligible domains.

```
$ python3 krawler
```

## Dependecy Graph
```
beautifulsoup4==4.11.1
  - soupsieve [required: >1.2, installed: 2.3.2.post1]
black==22.6.0
  - click [required: >=8.0.0, installed: 8.1.3]
  - mypy-extensions [required: >=0.4.3, installed: 0.4.3]
  - pathspec [required: >=0.9.0, installed: 0.9.0]
  - platformdirs [required: >=2, installed: 2.5.2]
  - tomli [required: >=1.1.0, installed: 2.0.1]
  - typing-extensions [required: >=3.10.0.0, installed: 4.3.0]
lxml==4.9.1
requests==2.28.1
  - certifi [required: >=2017.4.17, installed: 2022.6.15]
  - charset-normalizer [required: >=2,<3, installed: 2.1.0]
  - idna [required: >=2.5,<4, installed: 3.3]
  - urllib3 [required: >=1.21.1,<1.27, installed: 1.26.11]
validators==0.20.0
  - decorator [required: >=3.4.0, installed: 5.1.1]
```