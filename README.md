## 简介

使用FastAPI实现 [Vue Naive Admin](https://github.com/zclzone/vue-naive-admin) 后端接口
`Vue Naive Admin 是一款极简风格的后台管理模板，包含前后端解决方案，前端使用 Vite + Vue3 + Pinia + Unocss，后端使用 Nestjs + TypeOrm + MySql，简单易用，赏心悦目，历经十几次重构和细节打磨，诚意满满！！`


### 安装
```cmd
pip install -r requirements.txt
```
- 或使用pipenv创建
```cmd
pipenv install
```
### 配置数据库
* 重命名文件: config/setting.py 为 config/secure.py
### 初始化demo数据
```
python3 init_demo.py
```
### 运行
```cmd
python3 main.py
```
### 接口文档
项目运行后访问: [localhost/docs](http://localhost:8085/docs)

### 其他
可将编译后的Vue Naive Admin前端程序放在web目录下
