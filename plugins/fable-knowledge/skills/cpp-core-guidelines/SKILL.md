---
name: cpp-core-guidelines
description: Use when setting up or reviewing test/coverage/sanitizer tooling for modern C++ (C++17/20/23) projects — GoogleTest/CTest wiring, llvm-profdata/gcov coverage, and ASan/UBSan/TSan flags. Also covers a short list of C++ Core Guidelines rules whose correct answer contradicts a plausible guess.
---

# C++ Core Guidelines

Rule IDs reference the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines). Most rules (RAII, immutability, rule of zero/five, prefer `unique_ptr`, avoid raw `new`/`delete`, etc.) are standard knowledge and omitted here — this file covers only the rules where a plausible guess is wrong, plus the testing/tooling setup.

## Counterintuitive rules

| Rule | Plausible wrong guess | Actual behavior |
|------|------------------------|------------------|
| F.49 | Returning `const T` looks safer | It suppresses move construction on the return value — a pessimization, not a safety win |
| CP.44 | `std::lock_guard<std::mutex>(m);` locks for the statement | The unnamed temporary destructs immediately at the end of the full expression — no lock is held while the next line runs |
| CP.8 | `volatile` makes a variable thread-safe | `volatile` only affects compiler reordering/caching for hardware I/O; it gives no atomicity or memory-ordering guarantee across threads |
| SL.io.50 | `std::endl` is just a newline | `endl` forces a stream flush on every call; use `'\n'` and flush explicitly when needed |
| R.13 | Passing two `new`-expressions as arguments to the same call is fine | If one allocation succeeds and the sibling argument's allocation throws, the first leaks — evaluation order between arguments is unsequenced |
| T.144 | You can specialize a function template like a class template | Function template "specializations" don't participate in overload resolution the way overloads do and can't be partial — prefer plain overloads |
| F.53 | Capturing a local by reference in a lambda is safe if the lambda is short-lived | If that lambda is handed to another thread or stored for later (e.g. as a callback), the reference dangles once the enclosing scope returns |
| C.12 | `const` or reference data members just add safety | They also delete the compiler-generated copy assignment and both move operations |

## Testing infrastructure

### GoogleTest via CMake/CTest

```cmake
cmake_minimum_required(VERSION 3.20)
project(example LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
set(GTEST_VERSION v1.17.0)   # pin per project policy
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/${GTEST_VERSION}.zip
)
FetchContent_MakeAvailable(googletest)

add_executable(example_tests tests/calculator_test.cpp src/calculator.cpp)
target_link_libraries(example_tests GTest::gtest GTest::gmock GTest::gtest_main)

enable_testing()
include(GoogleTest)
gtest_discover_tests(example_tests)
```

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j
ctest --test-dir build --output-on-failure
ctest --test-dir build -R "UserStoreTest.*" --output-on-failure
./build/example_tests --gtest_filter=UserStoreTest.FindsExistingUser
```

### Coverage

Target-level flags, not global:

```cmake
option(ENABLE_COVERAGE "Enable coverage flags" OFF)
if(ENABLE_COVERAGE)
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    target_compile_options(example_tests PRIVATE --coverage)
    target_link_options(example_tests PRIVATE --coverage)
  elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(example_tests PRIVATE -fprofile-instr-generate -fcoverage-mapping)
    target_link_options(example_tests PRIVATE -fprofile-instr-generate)
  endif()
endif()
```

GCC + gcov + lcov:

```bash
cmake -S . -B build-cov -DENABLE_COVERAGE=ON
cmake --build build-cov -j
ctest --test-dir build-cov
lcov --capture --directory build-cov --output-file coverage.info
lcov --remove coverage.info '/usr/*' --output-file coverage.info
genhtml coverage.info --output-directory coverage
```

Clang + llvm-cov:

```bash
cmake -S . -B build-llvm -DENABLE_COVERAGE=ON -DCMAKE_CXX_COMPILER=clang++
cmake --build build-llvm -j
LLVM_PROFILE_FILE="build-llvm/default.profraw" ctest --test-dir build-llvm
llvm-profdata merge -sparse build-llvm/default.profraw -o build-llvm/default.profdata
llvm-cov report build-llvm/example_tests -instr-profile=build-llvm/default.profdata
```

### Sanitizers

```cmake
option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
option(ENABLE_UBSAN "Enable UndefinedBehaviorSanitizer" OFF)
option(ENABLE_TSAN "Enable ThreadSanitizer" OFF)

if(ENABLE_ASAN)
  add_compile_options(-fsanitize=address -fno-omit-frame-pointer)
  add_link_options(-fsanitize=address)
endif()
if(ENABLE_UBSAN)
  add_compile_options(-fsanitize=undefined -fno-omit-frame-pointer)
  add_link_options(-fsanitize=undefined)
endif()
if(ENABLE_TSAN)
  add_compile_options(-fsanitize=thread)
  add_link_options(-fsanitize=thread)
endif()
```
