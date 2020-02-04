# UCAS Affair Scripts

[![python](https://img.shields.io/badge/python-3.7-blue.svg)](https://github.com/zhangxu3486432/UCAS-Affair-Scripts)
[![python](https://img.shields.io/github/license/zhangxu3486432/UCAS-Affair-Scripts)](https://img.shields.io/github/license/zhangxu3486432/UCAS-Affair-Scripts)

开发/收集 中国科学院大学 各种事务的自动化脚本

已有脚本：

* 选课
* 监听成绩

期待贡献，添加更多有趣的脚本，kill TodoList item

> Warning:
>
> 由于 `选课系统` 只能单点登录，如果同时运行两个脚本，或者在运行脚本的时候登陆网页端，他们之前会争抢会话。
>
> 脚本默认在会话失效后再次自动获取，所以在刷课和监听成绩的过程中，如果您需要浏览选课系统的网页端，需要先暂停脚本。
>
> ```shell script
> kill -STOP $pid # suspend
> kill -CONT $pid # resume
> ```

## Usage

### Initialization

Pull project:

```shell script
git clone https://github.com/zhangxu3486432/UCAS-Affair-Scripts.git
```

Enter the working directory:

```shell script
cd UCAS-Affair-Scripts
```

Install dependency:

```shell script
pip3 install -r deploy/requirements.txt
```

### Configuration

> Set in the settings.py

Set `http://sep.ucas.ac.cn/` UserName and PassWord

```python
USERNAME = ''
PASSWORD = ''
```

### Login

> In the off-campus network login need to fill in the `Verification Code`. First login to save cookies in `sep.cookie`, so that you can facilitate deployment in the server.

```shell script
python3 login.py
```

The `Verification Code` picture is saved in verification.png, open the picture identification key and fill it in terminal.

![verification code](https://zhangxu3486432.github.io/static/images/verification.png)

As you can see, this `Verification Code` is `7351`.

Fill the `7351` in terminal and press enter.

![login input](https://zhangxu3486432.github.io/static/images/login.png)

### RUN take-courses

1. Set the courses which you want to take
    
    Examples:

    ```python
   COURSES = ['自然语言处理', '机器人智能控制', '积极心理学']
    ```
   
2. Fill in the college to which the course you choose belongs
        
    Examples:
    
    ```python
   COLLEGES = ['人工智能学院', '心理学系']
    ```

3. Run
    
    ```shell script
   python3 take_courses.py
    ```

### Run monitor_grades

1. Set email info

    > if you want to monitor your grads, you need to set it
    
    ```python
   SEND_EMAIL = ''
   SEND_EMAIL_PWD = ''
    
   RECEIVE_EMAIL = ''
    ```

2. Run

    ```shell script
   python3 monitor_grades.py
    ```

## TodoList

- [ ] Test and adapt to more python versions
- [ ] Shuttle Bus Reservation
- [ ] Build Docker Image
- [ ] Automatic Identification Verification Code
