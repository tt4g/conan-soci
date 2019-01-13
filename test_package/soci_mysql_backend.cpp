#include <soci/soci.h>
#include <soci/mysql/soci-mysql.h>

int main() {
    try {
        soci::session sql(soci::mysql,
                          "user='conan_soci_user' password='conan_soci_pass'"
                          " host='127.0.0.1' port=3306 dbname='conan_soci_test'"
                          " charset='utf8' connect_timeout=10");
    } catch (const soci::soci_error &ex) {
        // don't connect server in tests.
        // pass if compile succeeded.
        return 0;
    }

    return 1;
}
