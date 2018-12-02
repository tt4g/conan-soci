
## conanfile.txt

```
[requires]
zlib/1.2.11@conan/stable
OpenSSL/1.0.2p@conan/stable
mysql-connector-c/6.1.11@bincrafters/stable
SOCI/4.0.0@tt4g/stable

[build_requires]

[options]
zlib:shared=True
OpenSSL:shared=True
mysql-connector-c:shared=True
SOCI:soci_cxx_c11=False
SOCI:soci_static=False
SOCI:with_boost=False
SOCI:with_mysql=True

[generators]
cmake
```
