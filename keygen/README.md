# 使用环境
   
> `rsa_keygen` 和 `aes_keygen` 的运行环境为Linux

# rsa的der文件生成方式

以2048bit为例:

> openssl genrsa -out output.pem 2048

生成一个`output.pem`的pem格式文件，其中包含了加解密过程中需要用到的n, e, d这些大整数

> openssl rsa -in output.pem -outform der -out output.der

将上一步生成pem格式文件转换成der, 生成的文件为`output.der`

# 使用方法

切换到平台的相应目录, 运行相应的patch脚本即可

`` python [elf|macho|flash]_patch.py input_lib output_lib [--aes-enc aes_enc_key_file] [--aes-dec aes_dec_key_file] [--rsa-private rsa_private_key.der] [--rsa-public rsa_public_key.der] [-h] ``

* input_lib: 
    * Android: Android/native/jni/arm*/ 目录下的 `.a` 静态库文件
    * iOS: iOS/lib/  目录下的`.a`静态库文件
    * flash: flash/ 目录下的`.a`静态库文件

* output_lib: 指定修改后的输出文件
* --rsa-private: der格式的文件，其中客户端调用RSA时需要用到的私钥
* --rsa-public: der格式的文件，其中客户端调用RSA时需要用到的公钥
* --aes-enc: 存有aes加密函数所用的密钥内容的文件，需为32个字节，对应AES-256
* --aes-dec: 存有aes解密函数所用的密钥内容的文件，需为32个字节，对应AES-256
