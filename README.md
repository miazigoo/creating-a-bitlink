# Bitly URL shortener

Creates a bitlink. If the link is a bitlink, it shows the number of clicks

### How to install

* [Download the script](https://github.com/miazigoo/creating-a-bitlink.git) 
* [Register on the website](https://api-ssl.bitly.com/) - and get a token of the format: ```ecbb0fa2d11d009c022dd9042f7bbe28f0f3bb60``` (<=the token is not valid)
* In the folder with the script create a file ```.env``` and write it there: ```BITLY_TOKEN='YOUR_TOKEN' ```

Python3 should already be installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Run the file from the console:
```
python main.py your_link
```
### Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).
