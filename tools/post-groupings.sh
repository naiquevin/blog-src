#!/usr/bin/env bash

echo 'Categories'
echo '=========='
grep -h 'Category:' content/*.md  \
    | sed 's/Category: //' \
    | sed 's/, /\n/g' \
    | sort \
    | uniq -c

echo

echo 'Tags'
echo '===='
grep -h 'Tags:' content/*.md  \
    | sed 's/Tags: //' \
    | sed 's/, /\n/g' \
    | sort \
    | uniq -c
