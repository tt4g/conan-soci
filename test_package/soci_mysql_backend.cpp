#include <soci/soci.h>
#include <soci/mysql/soci-mysql.h>

#include <stdexcept>

int main() {
    soci::session sql(soci::mysql,
                      "user='conan_soci_user' password='conan_soci_pass'"
                      " host='127.0.0.1' port=3306 dbname='conan_soci_test'"
                      " charset='utf8' connect_timeout=10");

    int count = 0;
    sql << "select 1 as one", soci::into(count);

    if (count != 1) {
        throw std::runtime_error("count not equal to 1");
    }

    return 0;
}
