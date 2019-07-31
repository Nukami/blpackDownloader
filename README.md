# blpackDownloader

A downloader for blpack.com to download documents on wenku.baidu.com easily


# Usage
### Account setting
Set your user and password at 17/18 lines.  
e.g.:  
``` python
user = "403526350"
password = "459349"
```

### Check balance
python blpack.py balance  
python blpack.py  

### Download
python blpack.py [url] [directory]  

e.g.:
```
python blpack.py https://wenku.baidu.com/view/8c84c14017fc700abb68a98271fe910ef02dae50.html?from=search
python blpack.py https://wenku.baidu.com/view/8c84c14017fc700abb68a98271fe910ef02dae50.html?from=search E:\documents
```