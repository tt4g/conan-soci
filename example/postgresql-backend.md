## conanfile.txt

```
[requires]
SOCI/4.0.0@tt4g/stable
libpq/9.6.9@bincrafters/stable
OpenSSL/1.0.2p@conan/stable
zlib/1.2.11@conan/stable

[build_requires]

[options]
SOCI:shared=False
SOCI:soci_cxx_c11=False
SOCI:with_boost=False
SOCI:with_postgresql=True
libpq:shared=False
libpq:with_openssl=True
libpq:with_zlib=True
OpenSSL:shared=False
zlib:shared=False

[generators]
cmake
```
