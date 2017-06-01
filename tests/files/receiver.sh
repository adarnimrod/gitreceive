#!/bin/sh
set -eu

# This part was copied verbatim from
# https://github.com/progrium/gitreceive/wiki/TipsAndTricks
fetch_submodules () {
    # We reinitialize .git to avoid conflicts
    rm -fr .git
    # GIT_DIR is previously set by gitreceive to ".", we want it back to default
    # for this
    unset GIT_DIR
    git init .

    # We read the submodules from .gitmodules
    git config -f .gitmodules --get-regexp '^submodule\..*\.path$' |
        while read -r path_key path
        do
            rm -fr "$path"
            url_key="$(echo "$path_key" | sed 's/\.path/.url/')"
            url="$(git config -f .gitmodules --get "$url_key")"
            git submodule add "$url" "$path"
        done
}

# shellcheck disable=SC2034
repository="$1"
# shellcheck disable=SC2034
revision="$2"
# shellcheck disable=SC2034
username="$3"
# shellcheck disable=SC2034
fingerprint="$4"

mkdir -p /var/tmp/gitreceive
(
cd /var/tmp/gitreceive
echo '----> Unpacking ...'
tar -xf -
if [ -f .gitmodules ]
then
    echo '----> Fetching submodules ...'
    fetch_submodules
fi
if [ -f receiver ] && [ -x receiver ]
then
    echo '----> Running receiver ...'
    ./receiver
fi
echo '----> Cleanup ...'
)
rm -rf /var/tmp/gitreceive
echo '----> OK.'
