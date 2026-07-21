---
name: cpp-core-guidelines
description: Use when writing, reviewing, or refactoring modern C++ (C++17/20/23). Covers C++ Core Guidelines rule IDs with compact examples (P/I, F, C, R, ES, E, Con, CP, T, SL, Enum, SF/NL, Per) plus GoogleTest/CTest wiring, coverage, and sanitizer flags.
---

# C++ Core Guidelines

Rule IDs reference the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

## Cross-cutting themes

1. RAII everywhere (P.8, R.1, E.6, CP.20): bind resource lifetime to object lifetime
2. Immutability by default (P.10, Con.1-5, ES.25): `const`/`constexpr` first
3. Type safety (P.4, I.4, ES.46-49, Enum.3): compile-time error prevention
4. Express intent (P.3, F.1, NL.1-2, T.10)
5. Minimize complexity (F.2-3, ES.5, Per.4-5)
6. Value semantics over pointer semantics (C.10, R.3-5, F.20, CP.31)

## Philosophy and interfaces (P.*, I.*)

| Rule | Summary |
|------|---------|
| P.1 | Express ideas directly in code |
| P.3 | Express intent |
| P.4 | Ideally, a program should be statically type safe |
| P.5 | Prefer compile-time checking to run-time checking |
| P.8 | Don't leak any resources |
| P.10 | Prefer immutable data to mutable data |
| I.1 | Make interfaces explicit |
| I.2 | Avoid non-const global variables |
| I.4 | Make interfaces precisely and strongly typed |
| I.11 | Never transfer ownership by a raw pointer or reference |
| I.23 | Keep the number of function arguments low |

```cpp
// P.10 + I.4: immutable, strongly typed interface
struct Temperature { double kelvin; };
Temperature boil(const Temperature& water);

// Violations:
double boil(double* temp);   // unclear ownership, unclear units
int g_counter = 0;           // I.2: non-const global
```

## Functions (F.*)

| Rule | Summary |
|------|---------|
| F.1 | Package meaningful operations as carefully named functions |
| F.2 | A function should perform a single logical operation |
| F.3 | Keep functions short and simple |
| F.4 | If a function might be evaluated at compile time, declare it `constexpr` |
| F.6 | If your function must not throw, declare it `noexcept` |
| F.8 | Prefer pure functions |
| F.16 | "In" parameters: cheaply-copied types by value, others by `const&` |
| F.20 | "Out" values: prefer return values to output parameters |
| F.21 | Multiple "out" values: prefer returning a struct |
| F.43 | Never return a pointer or reference to a local object |

```cpp
// F.16
void print(int x);                        // cheap: by value
void analyze(const std::string& data);    // expensive: by const&
void transform(std::string s);            // sink: by value (will move)

// F.20 + F.21: return a struct, not output parameters
struct ParseResult { std::string token; int position; };
ParseResult parse(std::string_view input);              // good
void parse(std::string_view, std::string&, int&);       // avoid

// F.4 + F.8
constexpr int factorial(int n) noexcept {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}
static_assert(factorial(5) == 120);
```

Anti-patterns: returning `T&&` (F.45); `va_arg`/C variadics (F.55); reference captures in lambdas passed to other threads (F.53); returning `const T`, which inhibits move (F.49).

## Classes (C.*)

| Rule | Summary |
|------|---------|
| C.2 | `class` if an invariant exists; `struct` if members vary independently |
| C.9 | Minimize exposure of members |
| C.20 | If you can avoid defining default operations, do (Rule of Zero) |
| C.21 | If you define or `=delete` any copy/move/destructor, handle all five (Rule of Five) |
| C.35 | Base class destructor: public virtual or protected non-virtual |
| C.41 | A constructor should create a fully initialized object |
| C.46 | Declare single-argument constructors `explicit` |
| C.67 | A polymorphic class should suppress public copy/move |
| C.128 | Virtual functions: exactly one of `virtual`, `override`, `final` |

```cpp
// C.20 Rule of Zero: compiler-generated special members
struct Employee {
    std::string name;
    std::string department;
    int id;
};

// C.21 Rule of Five: resource-managing class defines all five
class Buffer {
public:
    explicit Buffer(std::size_t size)
        : data_(std::make_unique<char[]>(size)), size_(size) {}
    ~Buffer() = default;
    Buffer(const Buffer& other)
        : data_(std::make_unique<char[]>(other.size_)), size_(other.size_) {
        std::copy_n(other.data_.get(), size_, data_.get());
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            auto new_data = std::make_unique<char[]>(other.size_);
            std::copy_n(other.data_.get(), other.size_, new_data.get());
            data_ = std::move(new_data);
            size_ = other.size_;
        }
        return *this;
    }
    Buffer(Buffer&&) noexcept = default;
    Buffer& operator=(Buffer&&) noexcept = default;
private:
    std::unique_ptr<char[]> data_;
    std::size_t size_;
};

// C.35 + C.128
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;   // C.121: pure interface
};
class Circle : public Shape {
public:
    explicit Circle(double r) : radius_(r) {}
    double area() const override { return 3.14159 * radius_ * radius_; }
private:
    double radius_;
};
```

Anti-patterns: virtual calls in constructors/destructors (C.82); `memset`/`memcpy` on non-trivial types (C.90); different default args on virtual and overrider (C.140); `const` or reference data members, which suppress copy/move (C.12).

## Resource management (R.*)

| Rule | Summary |
|------|---------|
| R.1 | Manage resources automatically using RAII |
| R.3 | A raw pointer (`T*`) is non-owning |
| R.5 | Prefer scoped objects; don't heap-allocate unnecessarily |
| R.10 | Avoid `malloc()`/`free()` |
| R.11 | Avoid calling `new` and `delete` explicitly |
| R.20 | Use `unique_ptr` or `shared_ptr` to represent ownership |
| R.21 | Prefer `unique_ptr` over `shared_ptr` unless sharing ownership |
| R.22 | Use `make_shared()` to make `shared_ptr`s |

```cpp
auto widget = std::make_unique<Widget>("config");  // unique ownership
auto cache  = std::make_shared<Cache>(1024);       // shared ownership

// R.3: raw pointer = non-owning observer
void render(const Widget* w) { if (w) w->draw(); }
render(widget.get());

// R.1: RAII wrapper for a C resource
class FileHandle {
public:
    explicit FileHandle(const std::string& path)
        : handle_(std::fopen(path.c_str(), "r")) {
        if (!handle_) throw std::runtime_error("Failed to open: " + path);
    }
    ~FileHandle() { if (handle_) std::fclose(handle_); }
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&& other) noexcept
        : handle_(std::exchange(other.handle_, nullptr)) {}
    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) {
            if (handle_) std::fclose(handle_);
            handle_ = std::exchange(other.handle_, nullptr);
        }
        return *this;
    }
private:
    std::FILE* handle_;
};
```

Anti-patterns: naked `new`/`delete` (R.11); `malloc`/`free` in C++ (R.10); multiple allocations in one expression — exception-safety hazard (R.13); `shared_ptr` where `unique_ptr` suffices (R.21).

## Expressions and statements (ES.*)

| Rule | Summary |
|------|---------|
| ES.5 | Keep scopes small |
| ES.20 | Always initialize an object |
| ES.23 | Prefer `{}` initializer syntax |
| ES.25 | Declare objects `const` or `constexpr` unless modification is intended |
| ES.28 | Use lambdas for complex initialization of `const` variables |
| ES.45 | Avoid magic constants; use symbolic constants |
| ES.46 | Avoid narrowing/lossy arithmetic conversions |
| ES.47 | Use `nullptr` rather than `0` or `NULL` |
| ES.48 | Avoid casts |
| ES.50 | Don't cast away `const` |

```cpp
const int max_retries{3};
const std::vector<int> primes{2, 3, 5, 7, 11};

// ES.28: lambda for complex const initialization
const auto config = [&] {
    Config c;
    c.timeout = std::chrono::seconds{30};
    c.retries = max_retries;
    return c;
}();
```

Anti-patterns: uninitialized variables (ES.20); `0`/`NULL` as pointer (ES.47); C-style casts — use `static_cast` etc. (ES.48); casting away `const` (ES.50); magic numbers (ES.45); mixed signed/unsigned arithmetic (ES.100); name reuse in nested scopes (ES.12).

## Error handling (E.*)

| Rule | Summary |
|------|---------|
| E.1 | Develop an error-handling strategy early in a design |
| E.2 | Throw an exception to signal that a function can't perform its task |
| E.6 | Use RAII to prevent leaks |
| E.12 | Use `noexcept` when throwing is impossible or unacceptable |
| E.14 | Use purpose-designed user-defined types as exceptions |
| E.15 | Throw by value, catch by reference |
| E.16 | Destructors, deallocation, and swap must never fail |
| E.17 | Don't try to catch every exception in every function |

```cpp
class AppError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};
class NetworkError : public AppError {
public:
    NetworkError(const std::string& msg, int code)
        : AppError(msg), status_code(code) {}
    int status_code;
};

void run() {
    try {
        fetch_data("https://api.example.com");
    } catch (const NetworkError& e) {   // E.15: catch by reference
        log_error(e.what(), e.status_code);
    } catch (const AppError& e) {
        log_error(e.what());
    }
    // E.17: let unexpected errors propagate
}
```

Anti-patterns: throwing `int` or string literals (E.14); catching by value — slicing (E.15); empty catch blocks; exceptions as flow control (E.3); `errno`-style global error state (E.28).

## Constants and immutability (Con.*)

| Rule | Summary |
|------|---------|
| Con.1 | By default, make objects immutable |
| Con.2 | By default, make member functions `const` |
| Con.3 | By default, pass pointers and references to `const` |
| Con.4 | Use `const` for values that don't change after construction |
| Con.5 | Use `constexpr` for values computable at compile time |

```cpp
class Sensor {
public:
    explicit Sensor(std::string id) : id_(std::move(id)) {}
    const std::string& id() const { return id_; }        // Con.2
    double last_reading() const { return reading_; }
    void record(double value) { reading_ = value; }      // non-const only when mutating
private:
    const std::string id_;                               // Con.4
    double reading_{0.0};
};

void display(const Sensor& s);                           // Con.3
constexpr double PI = 3.14159265358979;                  // Con.5
```

## Concurrency (CP.*)

| Rule | Summary |
|------|---------|
| CP.2 | Avoid data races |
| CP.3 | Minimize explicit sharing of writable data |
| CP.4 | Think in terms of tasks, rather than threads |
| CP.8 | Don't use `volatile` for synchronization |
| CP.20 | Use RAII, never plain `lock()`/`unlock()` |
| CP.21 | Use `std::scoped_lock` to acquire multiple mutexes |
| CP.22 | Never call unknown code while holding a lock |
| CP.42 | Don't wait without a condition |
| CP.44 | Remember to name your `lock_guard`s and `unique_lock`s |
| CP.100 | Don't use lock-free programming unless you absolutely have to |

```cpp
class ThreadSafeQueue {
public:
    void push(int value) {
        std::lock_guard<std::mutex> lock(mutex_);  // CP.44: named
        queue_.push(value);
        cv_.notify_one();
    }
    int pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this] { return !queue_.empty(); });  // CP.42: with condition
        const int value = queue_.front();
        queue_.pop();
        return value;
    }
private:
    std::mutex mutex_;             // CP.50: mutex lives with its data
    std::condition_variable cv_;
    std::queue<int> queue_;
};

// CP.21: multiple mutexes, deadlock-free
void transfer(Account& from, Account& to, double amount) {
    std::scoped_lock lock(from.mutex_, to.mutex_);
    from.balance_ -= amount;
    to.balance_ += amount;
}
```

Anti-patterns: `volatile` for synchronization — it is for hardware I/O only (CP.8); detached threads (CP.26); unnamed lock guard `std::lock_guard<std::mutex>(m);` — the temporary destructs immediately, no locking (CP.44); holding locks across callbacks (CP.22); casual lock-free code (CP.100).

## Templates (T.*)

| Rule | Summary |
|------|---------|
| T.1 | Use templates to raise the level of abstraction |
| T.2 | Use templates to express algorithms for many argument types |
| T.10 | Specify concepts for all template arguments |
| T.11 | Use standard concepts whenever possible |
| T.13 | Prefer shorthand notation for simple concepts |
| T.43 | Prefer `using` over `typedef` |
| T.120 | Use template metaprogramming only when you really need to |
| T.144 | Don't specialize function templates (overload instead) |

```cpp
#include <concepts>

template<std::integral T>                  // T.10 + T.11
T gcd(T a, T b) {
    while (b != 0) a = std::exchange(b, a % b);
    return a;
}

// T.13: shorthand syntax
void sort(std::ranges::random_access_range auto& range) {
    std::ranges::sort(range);
}

template<typename T>
concept Serializable = requires(const T& t) {
    { t.serialize() } -> std::convertible_to<std::string>;
};
template<Serializable T>
void save(const T& obj, const std::string& path);
```

Anti-patterns: unconstrained templates in visible namespaces (T.47); specializing function templates (T.144); metaprogramming where `constexpr` suffices (T.120); `typedef` (T.43).

## Standard library (SL.*)

| Rule | Summary |
|------|---------|
| SL.1 | Use libraries wherever possible |
| SL.2 | Prefer the standard library to other libraries |
| SL.con.1 | Prefer `std::array` or `std::vector` over C arrays |
| SL.con.2 | Prefer `std::vector` by default |
| SL.str.1 | Use `std::string` to own character sequences |
| SL.str.2 | Use `std::string_view` to refer to character sequences |
| SL.io.50 | Avoid `endl` — use `'\n'`; `endl` forces a flush |

```cpp
const std::array<int, 4> fixed_data{1, 2, 3, 4};
std::string build_greeting(std::string_view name) {   // view observes, string owns
    return "Hello, " + std::string(name) + "!";
}
std::cout << "result: " << value << '\n';             // SL.io.50
```

## Enumerations (Enum.*)

| Rule | Summary |
|------|---------|
| Enum.1 | Prefer enumerations over macros |
| Enum.3 | Prefer `enum class` over plain `enum` |
| Enum.5 | Don't use ALL_CAPS for enumerators |
| Enum.6 | Avoid unnamed enumerations |

```cpp
enum class LogLevel { debug, info, warning, error };  // scoped, no ALL_CAPS
enum { RED, GREEN, BLUE };                            // Enum.3+5+6 violation
#define MAX_SIZE 100                                  // Enum.1 violation: use constexpr
```

## Source files and naming (SF.*, NL.*)

| Rule | Summary |
|------|---------|
| SF.1 | `.cpp` for code files, `.h` for interface files |
| SF.7 | Don't write `using namespace` at global scope in a header |
| SF.8 | Use `#include` guards for all `.h` files |
| SF.11 | Header files should be self-contained |
| NL.5 | No type info in names (no Hungarian notation) |
| NL.8 | Use a consistent naming style |
| NL.9 | ALL_CAPS for macro names only |
| NL.10 | Prefer `underscore_style` names |

```cpp
// SF.8 + SF.11
#ifndef PROJECT_MODULE_WIDGET_H
#define PROJECT_MODULE_WIDGET_H
#include <string>          // header includes what it needs

namespace project::module {
constexpr int max_buffer_size = 4096;   // NL.9: not a macro, not ALL_CAPS
class tcp_connection {                  // NL.10
public:
    void send_message(std::string_view msg);
private:
    std::string host_;                  // trailing underscore for members
};
}  // namespace project::module
#endif
```

Anti-patterns: `using namespace std;` in a header (SF.7); inclusion-order-dependent headers (SF.10-11); `strName`, `iCount` (NL.5).

## Performance (Per.*)

| Rule | Summary |
|------|---------|
| Per.1 | Don't optimize without reason |
| Per.2 | Don't optimize prematurely |
| Per.6 | Don't make claims about performance without measurements |
| Per.7 | Design to enable optimization |
| Per.10 | Rely on the static type system |
| Per.11 | Move computation from run time to compile time |
| Per.19 | Access memory predictably |

```cpp
// Per.11: compile-time lookup table
constexpr auto lookup_table = [] {
    std::array<int, 256> table{};
    for (int i = 0; i < 256; ++i) table[i] = i * i;
    return table;
}();

// Per.19: contiguous data is cache-friendly
std::vector<Point> points;                            // good
std::vector<std::unique_ptr<Point>> indirect_points;  // pointer chasing
```

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
