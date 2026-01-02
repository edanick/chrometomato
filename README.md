# Details

## Author: Edan
## Version: 1.0.8

A selenium wrapper with easy use, configuration and shorter code.
---

# Documentation

## Steps

### 1. Installation

> `pip install chrometomato`

### 2. Import

```python
from chrometomato import Chrome
```

# Initilization

`chrome_arguments.yaml`

> this file is to set the browser user agent and launch arguments

```yaml
user_agent: >-
    user agent string
options:
  - --mute-audio
```

`cookies.txt`

```
paste your cookies here
```

`example.py`

> Initiate the chrome driver with your custom user agent, launch options and load cookies for a specific domain based on the yaml and txt files

```python
from chrometomato import Chrome

chrome = Chrome('chrome_arguments.yaml', 'cookies.txt', 'example.com')
```

# Functions

## 1. get

> Navigate to a specific url

### Parameters

> Navigate to a url

`url` : str \
The url to navigate to

```python
chrome.get('example.com')
```
---

## 2. find_element

> Find a web element by a specific selection method

### Parameters

`sm`: sm \
Selection method (sm.CLASS, sm.ID, sm.NAME, sm.CSS_SELECTOR, sm.XPATH)

`value`: str \
A value of an id / class / name / css selector / xpath

`timeout`: int \
Timeout to wait for the element to be found until an error is being thrown if the element is not found

```python
from chrometomato import sm

element = chrome.find_element(sm.ID, 'element-id')
```

---

## 3. find_elements

> Find an array of web elements by a specific selection method

### Parameters

`sm`: sm \
Selection method

`value`: str \
The value to search for

`timeout`: int \
Timeout in seconds (default: 10)

```python
elements = chrome.find_elements(sm.CSS_SELECTOR, 'div.items')
```

---

## 4. element_exists

> Determine if an element exists in the page or not

### Parameters

`sm`: sm \
Selection method

`value`: str \
The value to search for

`timeout`: int \
Timeout in seconds (default: 10)

```python
if chrome.element_exists(sm.CLASS, 'my-class'):
    print("Element exists!")
```

---

## 5. click_element

> Find a web element and click it

### Parameters

`sm`: sm \
Selection method

`value`: str \
The value to search for

`timeout`: int \
Timeout in seconds (default: 10)

```python
chrome.click_element(sm.XPATH, '//button[@id="submit"]')
```

---

## 6. scroll_element

> Find a web element and scroll it until the end

### Parameters

`sm`: sm \
Selection method

`value`: str \
The value to search for

`timeout`: int \
Timeout in seconds (default: 10)

```python
chrome.scroll_element(sm.ID, 'scrollable-container')
```

---

## 7. wait

> Wait before executing a command

### Parameters

`seconds`: float \
Time in seconds to wait

```python
chrome.wait(5.5)
```

---

## 8. title

> Get the current title of the document

```python
print(chrome.title)
```

---

## 9. run

> Loop your function until you forcefully exit or call quit

### Parameters

`process`: function \
Infinite loop function that you want to run

`interval`: int \
Tickrate in seconds (default: 10)

```python
def loop():
    # your code here

chrome.run(loop, interval=5)
```

---

## 10. stays

> Prevent chrome from closing (keeps the script running)

```python
chrome.stays()
```

---

## 11. quit

> Close the web browser and stop the running loop

```python
chrome.quit()
```

