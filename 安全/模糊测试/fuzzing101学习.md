# fuzzing101学习

## Excercise 1 Xpdf

- 使用 afl 的一些编译器对源代码进行插桩编译

```
export LLVM_CONFIG="llvm-config-11"
CC=$HOME/AFLplusplus/afl-clang-fast CXX=$HOME/AFLplusplus/afl-clang-fast++ ./configure --prefix="$HOME/fuzzing_xpdf/install/"
make
make install
```

运行fuzzer

```
afl-fuzz -i $HOME/fuzzing_xpdf/pdf_examples/ -o $HOME/fuzzing_xpdf/out/ -s 123 -- $HOME/fuzzing_xpdf/install/bin/pdftotext @@ $HOME/fuzzing_xpdf/output
```

- -i indicates the directory where we have to put the input cases (a.k.a file examples)
- -o indicates the directory where AFL++ will store the mutated files
- -s indicates the static random seed to use
- @@ is the placeholder target's command line that AFL will substitute with each input file name

使用 gdb 进行调试

```bash
gdb --args $HOME/fuzzing_xpdf/install/bin/pdftotext $HOME/fuzzing_xpdf/out/default/crashes/<your_filename> $HOME/fuzzing_xpdf/output
```

运行

```bash
run
```

回溯（backtrace）
```bash
bt
```

## Excercise 2 libexif

- 使用外部库的



## Exercise 3 TCPdump

- 使用 ASan 进行fuzz

