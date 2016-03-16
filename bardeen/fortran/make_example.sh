
# add dependencies in the correct order
dependencies="tricks
fft"
# directory for tmp files (should be separate! it's deleted afterwards!)
TMP=forttmp

/bin/rm -rf "$TMP" *.run
mkdir -p "$TMP/debug" "$TMP/opt" "$TMP/fort"

# uncomment optimized lines to create optimized version
for dep in $dependencies
do
	echo "compile $dep"
	expand --tabs=2 "$dep.f03" > "$TMP/fort/$dep.F03" || exit 1
	gfortran --free-form -fmax-errors=1 $(printf -- '-J%s/debug' "$TMP") -Wall -Wextra -pedantic -fbacktrace -fbounds-check -ffpe-trap=zero,overflow "$TMP/fort/$dep.F03" -lblas -llapack -fopenmp -lgomp -c -o "$TMP/debug/$dep.o"  || exit 2
	gfortran --free-form -fmax-errors=1 $(printf -- '-J%s/opt'   "$TMP") -Wall -Wextra -pedantic -O3 -march=native                                   "$TMP/fort/$dep.F03" -lblas -llapack -fopenmp -lgomp -c -o "$TMP/opt/$dep.o"    || exit 3
done
echo "compile main"
expand --tabs=2 "main.f03" > "$TMP/fort/main.F03" || exit 4
gfortran --free-form -fmax-errors=1 $(printf -- '-J%s/debug' "$TMP") -Wall -Wextra -pedantic -fbacktrace -fbounds-check -ffpe-trap=zero,overflow "$TMP/fort/main.F03" $(sed -e "s/^/$TMP\/debug\//" -e "s/$/.o/" <<< "$dependencies") -lblas -llapack -fopenmp -lgomp -o debug.run || exit 5
gfortran --free-form -fmax-errors=1 $(printf -- '-J%s/opt' "$TMP")   -Wall -Wextra -pedantic -O3 -march=native                                   "$TMP/fort/main.F03" $(sed -e "s/^/$TMP\/opt\//"   -e "s/$/.o/" <<< "$dependencies") -lblas -llapack -fopenmp -lgomp -o opt.run     || exit 6
/bin/rm -rf "$TMP"
echo "made" $(ls *.run)


