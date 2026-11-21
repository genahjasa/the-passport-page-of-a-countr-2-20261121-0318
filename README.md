# The Passport Page of a Country That Isn't There

![make.fun rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)
![make.fun reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg?variant=reward)
![make.fun rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg?variant=rank)

Entry for the make.fun competition **the-passport-page-of-a-countr-2-20261121-0318**
("The Passport Page of a Country That Isn't There", $50 prize).

## What it is

An invented passport spread for **The Republic of Auralia** — a country
that does not exist. Deep teal and gold, ornate guilloche pattern, a
portrait photo area, an invented script and coat of arms, and visa stamps:
elegant, slightly whimsical, photorealistic document style.

## How it works

`main.py` (pure Python 3.13 standard library, no network) validates the
bundled artwork `image.jpg` — well-formed JPEG, under 1 MiB, at most
1024×1024 — then copies it byte-for-byte to `entry.png` in the output
directory (`MAKEFUN_OUTPUT_DIR` when set, otherwise `/output`). The run is
deterministic: two runs produce byte-identical output. If validation fails,
nothing is written.

## Run / verify

```sh
python3 -m py_compile main.py
MAKEFUN_OUTPUT_DIR=/tmp/passport-out python3 main.py
sha256sum /tmp/passport-out/entry.png
```

Run it twice and compare the hashes — they must match.

## License

MIT — see [LICENSE](LICENSE).
