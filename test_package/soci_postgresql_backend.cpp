#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>

int main() {
    try {
        soci::session sql(soci::postgresql,
                          "user='conan_soci_user' password='conan_soci_pass'"
                          " host='127.0.0.1' port=5432 dbname='conan_soci_test'"
                          " application_name='conan_soci' connect_timeout=10"
                          " options='-c client_encoding=utf8'");
    } catch (const soci::soci_error &/* ex */) {
        // don't connect server in tests.
        // pass if compile succeeded.
        return 0;
    }

    return 1;
}
