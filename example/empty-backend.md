## conanfile.txt

```
[requires]
SOCI/4.0.0@tt4g/stable

[build_requires]

[options]
SOCI:soci_cxx_c11=False
SOCI:soci_static=False
SOCI:with_boost=False
SOCI:soci_empty=True

[generators]
cmake

```

### Without empty backend

```
[requires]
zlib/1.2.11@conan/stable
OpenSSL/1.0.2p@conan/stable
libpq/9.6.9@bincrafters/stable
SOCI/4.0.0@tt4g/stable

[build_requires]

[options]
zlib:shared=True
OpenSSL:shared=True
libpq:shared=True
libpq:with_openssl=True
libpq:with_zlib=True
SOCI:soci_cxx_c11=False
SOCI:soci_static=False
SOCI:with_boost=False
SOCI:soci_empty=False
SOCI:with_postgresql=True

[generators]
cmake

```
