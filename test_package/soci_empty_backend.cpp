#include <soci/soci.h>
#include <soci/empty/soci-empty.h>

int main() {
    const soci::backend_factory &backendFactory = *soci::factory_empty();

    soci::session sql(backendFactory, "dummy connection");

    sql << "select 1 as one";
}
