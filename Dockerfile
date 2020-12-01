#FROM 指令指定基础镜像 
#比较常用的基础镜像有 ubuntu，centos。这里使用了一个极小的基础镜像 alpine 
FROM alpine:latest

#MAINTAINER 指令用于将镜像制作者相关的信息写入到镜像中 
#您可以将您的信息填入 name 以及 email 
MAINTAINER name<email>
#RUN 指令可以运行任何被基础 image 支持的命令，就像在操作系统上直接执行命令一样（如果使用 ubuntu 为基础镜像，这里应该用 apt-get 命令安装）
#安装 nginx 

RUN apk --update add nginx
RUN apt install python==3.7
RUN pip install tensorflow==1.14
RUN pip install numpy==2.1.5

#配置 Nginx，并设置在标准输出流输出日志（这样执行容器时才会看到日志） 
RUN sed-i"s#root html;#root /usr/share/nginx/html;#g" /etc/nginx/nginx.conf

#Nginx 日志输出到文件 
RUNln-sf/dev/stdout/var/log/nginx/access.log\ &&ln-sf/dev/stderr/var/log/nginx/error.log

#COPY 指令复制主机的文件到镜像中 （在这里当前路径就是 repo 根目录） 
#将 2048 项目的所有文件加入到 Nginx 静态资源目录里 
COPY./usr/share/nginx/html

#EXPOSE：指定容器监听的端口 
EXPOSE 8080
#CMD 指令，容器启动时执行的命令
#启动 Nginx 并使其保持在前台运行 
#CMD 一般是保持运行的前台命令，命令退出时容器也会退出 
CMD["nginx","-g", "pid/tmp/nginx.pid;daemonoff;"]
