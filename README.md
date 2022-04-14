<h3>Requirement</h3>
<ul>
    <li>Python 3.8.9 以上</li>
    <li>Pipenv</li>
</ul>


<h3>Install</h3>
* Install Pipenv
  
  ```
  pip3 install pipenv
  ```

* Install project dependencies

  ```
  pipenv install
  ```

<h3>設定</h3>
新增 .env file 在 Project 底下

```
# wordpress database 的 config
MYSQL_HOST=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_PORT=
# 上傳到 production 的設定
PRODUCTION_DOMAIN=
LOG_PRODUCTION_FILE_PATH=
# 上傳到 staging 的設定
STAGING_DOMAIN=
LOG_STAGING_FILE_PATH=
```

### 如果不想想上傳到 staging，請修改 main.py

```python
if __name__ == '__main__':
    ...
    # 把這行刪掉
    # main("staging", now)
    ...
```

---

<h3>執行</h3>

```
python3 -i main.py
```

<h3>設定排程</h3>

```
1. crontab -e                     #修改排程
2. 把這行加進去前, 請注意 project 的執行路徑是否正確 
"0 04 * * * cd /root/blog_crawl && /usr/bin/python3 /root/blog_crawl/main.py >> /var/log/cron.log 2>&1"
3. /etc/init.d/cron reload        #Reload crontab.
```