# accela

basic directory-based blog. i wanted a website that could easily display text without requiring a database or extra scripts

## Config

you can setup config information in `config.yaml`. for example:

```
ignore_file: .ignore    # this is an optional file placed in each directory to hide specific folders/files
ignore: [".ignore","favicon.ico","index.md"] # this is global ignored files
author: emily # this is for open graph protocol
```

each `index.md` accepts variables at the top of the file. this is for open graph protocol:

```
title: d&g & brain chemistry
description: comparing the transcendental unconscious with neurotransmitter receptors
```

you can sort directories by appending a number in front of them. note: the numbers will be stripped in url/display. check repository for example. use `index.md` to set page information.

## setup

- `docker build -t accela .`
- `docker run -p 80:80 accela` with any flags you want

---

design inspired by: `echo "c3lua3JldGllLm5ldAo=" | base64 -d`
