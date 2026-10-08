#pragma once

#include <string_view>

namespace openscore_native {

/// Returns the version of the starter native component.
/// Inputs: none. Outputs: stable version string view.
std::string_view version() noexcept;

}  // namespace openscore_native
