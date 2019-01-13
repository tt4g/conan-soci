#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>

#include <stdexcept>

int main() {
    soci::session sql(soci::postgresql,
                      "user='conan_soci_user' password='conan_soci_pass'"
                      " host='127.0.0.1' port=5432 dbname='conan_soci_test'"
                      " application_name='conan_soci' connect_timeout=10"
                      " options='-c client_encoding=utf8'");

    int count = 0;
    sql << "select 1 as one", soci::into(count);

    if (count != 1) {
        throw std::runtime_error("count not equal to 1");
    }

    return 0;
}
