#include "openscore_native/version.hpp"

int main() {
    return openscore_native::version() == "0.0.4" ? 0 : 1;
}
