---
name: perl-modern
description: Use when writing or reviewing Perl 5.32+ code and unsure which feature is available in which version, or when porting legacy Perl idioms forward. Covers the version-gated feature table (5.32/5.36/5.38/5.40) and the legacy-to-modern anti-pattern mapping.
---

# Modern Perl

## Version-gated features

| Feature | Since | Notes |
|---|---|---|
| `isa` infix operator | 5.32 | replaces `blessed($o) && $o->isa('X')` |
| `use v5.36` baseline | 5.36 | enables strict, warnings, signatures, `say` |
| `builtin 'true', 'false'` | 5.36 | experimental |
| `for_list` (multi-var for) | 5.36 | experimental in 5.36, stable in 5.40 |
| `class`/`field`/`method` (Corinna) | 5.38 | `use feature 'class'; no warnings 'experimental::class';` |
| native `try`/`catch` | 5.40 | stable; earlier versions use Try::Tiny |

## Legacy-to-modern conversion

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

## Gotcha

Deep hash/array access via arrow chains is safe by default on read: `$config->{cache}{host}` returns `undef` without error if any intermediate level doesn't exist — no autovivification happens on a plain read, only on assignment (`$config->{cache}{host} = 'x'` does create the intermediate levels).
