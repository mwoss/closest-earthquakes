## earthquake-detector
#### How to run
Create virtaul env using your favourite tool (pyenv, virtualenv, etc.) or just use base interpreter, then type:
```angular2html
$> pip install -r requirements.txt
$> python nearby_earthquakes.py latitude longitude
```
You can use -h for help. 
```angular2html
$> python nearby_earthquakes.py -h
```

If you want to run test just simply install requirements and type:
```angular2html
$> tox
```
<b>Code tested on Python 3.6.6</b>
#### Possible improvements/different approaches:
- Quickselect algorithm  
- Simple earthquake sorting  
- Build sorted list using bisect module  
- Sorted collection from sortedcollections library  
- Instroselect algorithm
