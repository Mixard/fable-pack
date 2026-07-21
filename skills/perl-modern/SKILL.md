---
name: perl-modern
description: Use when writing, reviewing, or securing Perl 5.32+ code. Covers modern idioms (signatures, postfix deref, Moo, class/field, try/catch), taint mode and injection-safe patterns, and Test2::V0 testing with prove and Devel::Cover.
---

# Modern Perl

## Idioms

### Version-gated features

| Feature | Since | Notes |
|---|---|---|
| `isa` infix operator | 5.32 | replaces `blessed($o) && $o->isa('X')` |
| `use v5.36` baseline | 5.36 | enables strict, warnings, signatures, `say` |
| `builtin 'true', 'false'` | 5.36 | experimental |
| `for_list` (multi-var for) | 5.36 | experimental in 5.36, stable in 5.40 |
| `class`/`field`/`method` (Corinna) | 5.38 | `use feature 'class'; no warnings 'experimental::class';` |
| native `try`/`catch` | 5.40 | stable; earlier versions use Try::Tiny |

### Preamble and signatures

`use v5.36` replaces the legacy boilerplate (`use strict; use warnings; use feature 'say', 'signatures'; no warnings 'experimental::signatures';`).

```perl
use v5.36;

sub connect_db($host, $port = 5432, $timeout = 30) {   # defaults, arity-checked
    return DBI->connect("dbi:Pg:host=$host;port=$port", undef, undef,
        { RaiseError => 1, PrintError => 0 });
}

sub log_message($level, @details) {                    # slurpy param
    say "[$level] " . join(' ', @details);
}
```

### Context and dereferencing

```perl
my @items = (1, 2, 3, 4, 5);
my @copy  = @items;      # list context: elements
my $count = @items;      # scalar context: 5

my @users = $data->{users}->@*;            # postfix deref (readable in chains)
my @roles = $data->{users}[0]{roles}->@*;
my %first = $data->{users}[0]->%*;

# Slices
@subset{qw(host port)} = @{$config->{database}}{qw(host port)};
my @first_two = $config->{database}{options}->@[0, 1];

# Multi-variable for (experimental 5.36, stable 5.40)
use feature 'for_list';
no warnings 'experimental::for_list';
for my ($key, $val) (%$config) { say "$key => $val" }
```

Deep hash access is safe by default: `$config->{cache}{host}` returns undef without error if any level is missing.

### Error handling

```perl
# eval/die
my $content = eval { path($path)->slurp_utf8 };
die "Config error: $@" if $@;

# Try::Tiny (pre-5.40)
use Try::Tiny;
my $user = try { $db->resultset('User')->find($id) // die "not found\n" }
           catch { warn "fetch failed: $_"; undef };

# Native try/catch (5.40+)
use v5.40;
sub divide($x, $y) {
    try { die "Division by zero" if $y == 0; return $x / $y }
    catch ($e) { warn "Error: $e"; return }
}
```

### OO: Moo and native class

Moo for lightweight modern OO; Moose only when its metaprotocol is needed. Blessed hashrefs give no validation or accessors.

```perl
package User;
use Moo;
use Types::Standard qw(Str Int ArrayRef);
use namespace::autoclean;

has name  => (is => 'ro', isa => Str, required => 1);
has email => (is => 'ro', isa => Str, required => 1);
has age   => (is => 'ro', isa => Int, default  => sub { 0 });
has roles => (is => 'ro', isa => ArrayRef[Str], default => sub { [] });

sub is_admin($self) { grep { $_ eq 'admin' } $self->roles->@* }
1;
```

Roles:

```perl
package Role::Serializable;
use Moo::Role;
use JSON::MaybeXS qw(encode_json);
requires 'TO_HASH';
sub to_json($self) { encode_json($self->TO_HASH) }
1;

package User;
use Moo;
with 'Role::Serializable';
sub TO_HASH($self) { { name => $self->name, email => $self->email } }
```

Native `class` keyword (5.38+, Corinna):

```perl
use v5.38;
use feature 'class';
no warnings 'experimental::class';

class Point {
    field $x :param;
    field $y :param;
    method magnitude() { sqrt($x**2 + $y**2) }
}
Point->new(x => 3, y => 4)->magnitude;   # 5
```

### Regexes

```perl
# Named captures + /x
my $log_re = qr{
    ^ (?<timestamp> \d{4}-\d{2}-\d{2} \s \d{2}:\d{2}:\d{2} )
    \s+ \[ (?<level> \w+ ) \]
    \s+ (?<message> .+ ) $
}x;
say "Time: $+{timestamp}, Level: $+{level}" if $line =~ $log_re;

# Precompile once with qr// when reused
my $email_re = qr/^[A-Za-z0-9._%+-]+\@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
```

### Files

```perl
use autodie;   # core; removes 'or die' noise

open my $fh, '<:encoding(UTF-8)', $path;   # three-arg open, lexical handle
local $/;
my $content = <$fh>;

# Path::Tiny for most file work
use Path::Tiny;
my $file = path('config', 'app.json');
my $content = $file->slurp_utf8;
$file->spew_utf8($new_content);
for my $child (path('src')->children(qr/\.pl$/)) { say $child->basename }
```

Two-arg `open FH, $path` and `open FH, "< $path"` allow shell/mode injection via user data (see Security).

### Modules and tooling

```perl
package MyApp::Util;
use v5.36;
use Exporter 'import';
our @EXPORT_OK   = qw(trim);
our %EXPORT_TAGS = (all => \@EXPORT_OK);
sub trim($str) { $str =~ s/^\s+|\s+$//gr }
1;
```

`.perltidyrc`:

```text
-i=4 -l=100 -ci=4 -ce -bar -nolq
```

Dependencies via cpanfile + Carton:

```bash
cpanm App::cpanminus Carton
carton install
carton exec -- perl bin/myapp
```

```perl
# cpanfile
requires 'Moo', '>= 2.005';
requires 'Path::Tiny';
on test => sub { requires 'Test2::V0'; requires 'Test::MockModule' };
```

### Legacy-to-modern conversion

| Legacy | Modern |
|---|---|
| `use strict; use warnings;` | `use v5.36;` |
| `my ($x, $y) = @_;` | `sub foo($x, $y) { ... }` |
| `@{ $ref }` / `%{ $ref }` | `$ref->@*` / `$ref->%*` |
| `open FH, "< $file"` | `open my $fh, '<:encoding(UTF-8)', $file` |
| blessed hashref | Moo class with types |
| `$1, $2, $3` | `$+{name}` named captures |
| `eval { }; if ($@)` | Try::Tiny or native try/catch (5.40+) |
| `BEGIN { require Exporter }` | `use Exporter 'import';` |
| manual file ops | Path::Tiny |
| `blessed($o) && $o->isa('X')` | `$o isa 'X'` (5.32+) |

### Anti-patterns

```perl
open FH, $filename;                     # two-arg open: injection risk
my $obj = new Foo(bar => 1);            # indirect object syntax; use Foo->new
no strict 'refs';                       # symbolic refs; use a hash instead
our $TIMEOUT = 30;                      # mutable global config; use constant or Moo attr
eval "require $module";                 # string eval: code injection
use Module::Runtime 'require_module';   # safe dynamic loading
require_module($module);
```

## Security

### Taint mode

`-T` tracks data from outside the program (argv, env, stdin, network) and blocks it from unsafe operations until explicitly untainted.

```perl
#!/usr/bin/perl -T
use v5.36;

# All tainted: $ARGV[0], $ENV{PATH}, <STDIN>, $ENV{QUERY_STRING}
# Taint mode requires sanitizing PATH first:
$ENV{PATH} = '/usr/local/bin:/usr/bin:/bin';
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
```

Untainting works by capturing through a regex; the capture group `$1` is untainted:

```perl
sub untaint_username($input) {
    if ($input =~ /^([a-zA-Z0-9_]{3,30})$/) { return $1 }
    die "Invalid username\n";
}

sub untaint_filename($input) {
    if ($input =~ m{^([a-zA-Z0-9._-]+)$}) { return $1 }
    die "Invalid filename\n";
}

# Pointless untaint — accepts anything, defeats the mechanism:
$input =~ /^(.*)$/s; return $1;
```

### Allowlist validation

Blocklists miss encoded attacks; allowlists define exactly what passes.

```perl
sub validate_sort_field($field) {
    my %allowed = map { $_ => 1 } qw(name email created_at updated_at);
    die "Invalid sort field: $field\n" unless $allowed{$field};
    return $field;
}

sub validate_integer($input) {
    if ($input =~ /^(-?\d{1,10})$/) { return $1 + 0 }
    die "Invalid integer\n";
}
```

### ReDoS

Nested quantifiers on overlapping patterns cause exponential backtracking:

```perl
qr/^(a+)+$/;          # vulnerable: nested quantifiers
qr/^([a-zA-Z]+)*$/;   # vulnerable
qr/^(.*?,){10,}$/;    # vulnerable: repeated greedy/lazy combo

qr/^a+$/;             # safe: single quantifier
qr/^[a-zA-Z]++$/;     # possessive quantifier (5.10+), no backtracking
qr/^(?>a+)$/;         # atomic group
```

For untrusted patterns, wrap the match in `local $SIG{ALRM}` + `alarm($timeout)`.

### Safe file operations

```perl
use Fcntl qw(:DEFAULT :flock);
use File::Spec;
use Cwd qw(realpath);

# Atomic creation (TOCTOU-safe)
sysopen(my $fh, $path, O_WRONLY | O_CREAT | O_EXCL, 0600)
    or die "Cannot create '$path': $!\n";

# Path traversal check: resolved path stays under base dir
sub safe_path($base_dir, $user_path) {
    my $real = realpath(File::Spec->catfile($base_dir, $user_path))
        // die "Path does not exist\n";
    my $base_real = realpath($base_dir) // die "Base dir does not exist\n";
    die "Path traversal blocked\n" unless $real =~ /^\Q$base_real\E(?:\/|\z)/;
    return $real;
}
```

`File::Temp` `tempfile(UNLINK => 1)` for temp files; `flock(LOCK_EX)` against races.

### Safe process execution

String-form `system("grep -r '$pattern' ...")` and backticks with interpolation go through the shell — injection via metacharacters. List form bypasses the shell:

```perl
system('grep', '-r', $user_pattern, '/var/log/app/') == 0
    or die "Command failed\n";

# Capture output safely
use IPC::Run3;
sub capture_output(@cmd) {
    my ($stdout, $stderr);
    run3(\@cmd, \undef, \$stdout, \$stderr);
    die "Command failed (exit $?): $stderr\n" if $?;
    return $stdout;
}
```

`Capture::Tiny` is an alternative for capturing stdout/stderr.

### SQL injection: DBI placeholders

```perl
my $dbh = DBI->connect($dsn, $user, $pass,
    { RaiseError => 1, PrintError => 0, AutoCommit => 1 });

# Placeholders for all values
my $sth = $dbh->prepare('SELECT * FROM users WHERE email = ?');
$sth->execute($email);
my $row = $sth->fetchrow_hashref;

$dbh->prepare('SELECT * FROM users WHERE name LIKE ? AND status = ?')
    ->execute("%$name%", $status);

# Interpolation is the vulnerability:
# $dbh->prepare("SELECT * FROM users WHERE email = '$email'")  # SQLi
```

Placeholders cannot parameterize identifiers — column/direction names need an allowlist:

```perl
sub order_by($dbh, $column, $direction) {
    my %allowed_cols = map { $_ => 1 } qw(name email created_at);
    my %allowed_dirs = map { $_ => 1 } qw(ASC DESC);
    die "Invalid column\n"    unless $allowed_cols{$column};
    die "Invalid direction\n" unless $allowed_dirs{uc $direction};
    my $sth = $dbh->prepare("SELECT * FROM users ORDER BY $column $direction");
    $sth->execute;
    return $sth->fetchall_arrayref({});
}
```

DBIx::Class generates parameterized queries from its search syntax (`{ email => { -like => '...' } }`).

### Output encoding

Encode per context: `HTML::Entities::encode_entities()` for HTML, `URI::Escape::uri_escape_utf8()` for URLs, `JSON::MaybeXS::encode_json()` for JSON. Mojolicious `<%= %>` auto-escapes, `<%== %>` is raw; Template Toolkit needs explicit `[% var | html %]`.

### perlcritic security policies

```ini
# .perlcriticrc
severity = 3
theme = security + core

[InputOutput::RequireThreeArgOpen]
severity = 5

[InputOutput::RequireCheckedSyscalls]
functions = :builtins
severity = 4

[BuiltinFunctions::ProhibitStringyEval]
severity = 5

[InputOutput::ProhibitBacktickOperators]
severity = 4

[Modules::RequireTaintChecking]
severity = 5

[InputOutput::ProhibitTwoArgOpen]
severity = 5

[InputOutput::ProhibitBarewordFileHandles]
severity = 5
```

General-purpose additions:

```ini
[InputOutput::RequireCheckedSyscalls]
functions = :builtins
exclude_functions = say print

[Subroutines::ProhibitExplicitReturnUndef]
severity = 4

[ValuesAndExpressions::ProhibitMagicNumbers]
allowed_values = 0 1 2 -1
```

```bash
perlcritic --severity 3 --theme security lib/
perlcritic --severity 4 --theme security --quiet lib/ || exit 1   # CI gate
```

## Testing

### Test2::V0

Modern replacement for Test::More: richer deep comparison, better diagnostics, backward-compatible.

```perl
use v5.36;
use Test2::V0;

# Hash builder — partial structure check
is($user->to_hash, hash {
    field name  => 'Alice';
    field email => match(qr/\@example\.com$/);
    field age   => validator(sub { $_ >= 18 });
    etc();                       # ignore other fields
}, 'user has expected fields');

# Array builder
is($result, array {
    item 'first';
    item match(qr/^second/);
    item DNE();                  # Does Not Exist — no extra items
}, 'matches expected list');

# Bag — order-independent
is($tags, bag { item 'perl'; item 'testing'; item 'tdd' }, 'all tags, any order');

# Exceptions
like(dies { divide(10, 0) }, qr/Division by zero/, 'dies on zero');
ok(lives { divide(10, 2) }, 'division succeeds') or note($@);

# Warnings
my $warnings = warns { User->new(name => '', email => 'bad') };

subtest 'User creation' => sub {
    my $user = User->new(name => 'Alice', email => 'alice@example.com');
    is($user->name, 'Alice', 'name is set');
};

done_testing;
```

`done_testing` at the end verifies all tests actually ran; without it, silently skipped test code goes unnoticed.

Test::More equivalents still seen in existing suites: `is/isnt`, `ok`, `is_deeply`, `like/unlike`, `isa_ok`, `can_ok`, plus `SKIP: { skip 'reason', $count unless $cond; ... }` and `TODO: { local $TODO = 'reason'; ... }`.

### Layout and prove

```text
t/
├── 00-load.t              # modules compile
├── unit/                  # per-module unit tests
├── integration/
├── lib/TestHelper.pm      # shared helpers, loaded via: use lib 't/lib'
└── fixtures/
```

```bash
prove -l t/                 # -l adds lib/ to @INC (without it, modules not found)
prove -lv t/unit/user.t     # verbose, single file
prove -lr t/                # recursive
prove -lr -j8 t/            # parallel, 8 jobs
prove -l --state=failed t/  # rerun only last failures
prove -l --color --timer t/
prove -l --formatter TAP::Formatter::JUnit t/ > results.xml   # CI
```

`.proverc`:

```text
-l
--color
--timer
-r
-j4
--state=save
```

### Fixtures and mocking

```perl
use File::Temp qw(tempdir);
subtest 'file processing' => sub {
    my $dir = tempdir(CLEANUP => 1);            # auto-teardown
    path($dir, 'input.txt')->spew_utf8("line1\nline2\nline3\n");
    is(process_file("$dir/input.txt")->{line_count}, 3, 'counts lines');
};
```

```perl
use Test::MockModule;
my $mock = Test::MockModule->new('MyApp::API');
$mock->mock(fetch_user => sub ($self, $id) {
    return { id => $id, name => 'Mock User' };
});
# Restored automatically when $mock goes out of scope.
# Direct glob assignment (*MyApp::API::fetch_user = sub {...}) leaks across tests.

my $call_count = 0;
$mock->mock(fetch_user => sub { $call_count++; return {} });
```

`Test::MockObject` builds injectable doubles (`->mock()`, `->called_ok()`). In-memory SQLite (`dbi:SQLite:dbname=:memory:`) works well for DB integration tests.

Gotchas: use `my` (not `our`) inside subtests to avoid state leaking; mock the dependency, not the code under test.

### Coverage with Devel::Cover

```bash
cover -test                                  # run tests with coverage

perl -MDevel::Cover -Ilib t/unit/user.t      # or step by step
cover

cover -report html                           # cover_db/coverage.html
cover -test -report text | grep 'Total'

# CI threshold gate
cover -test && cover -report text -select '^lib/' \
  | perl -ne 'if (/Total.*?(\d+\.\d+)/) { exit 1 if $1 < 80 }'
```
