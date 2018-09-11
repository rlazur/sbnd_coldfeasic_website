#!/bin/bash

for fn in j2/*.html; do
    mv $fn $fn".j2"
done

test_sbnd

for fn in j2/*.html.j2; do
    fn2=${fn::-3}
    mv $fn $fn2
done
