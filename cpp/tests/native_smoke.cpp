#include "openscore_native/version.hpp"

int main() {
    return openscore_native::version() == "0.0.1" ? 0 : 1;
}
