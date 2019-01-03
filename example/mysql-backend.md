
## conanfile.txt

```
[requires]
SOCI/4.0.0@tt4g/stable
mysql-connector-c/6.1.11@bincrafters/stable
OpenSSL/1.0.2p@conan/stable
zlib/1.2.11@conan/stable

[build_requires]

[options]
SOCI:soci_cxx_c11=False
SOCI:soci_static=False
SOCI:with_boost=False
SOCI:with_mysql=True
mysql-connector-c:shared=True
mysql-connector-c:with_ssl=True
mysql-connector-c:with_zlib=True
OpenSSL:shared=True
zlib:shared=True

[generators]
cmake
```
