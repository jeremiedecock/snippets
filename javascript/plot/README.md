## ObservableHQ Plot

https://observablehq.com/plot/getting-started


## Display snippets locally

### With Python

```
python3 -m http.server
```

to display snippets on 0.0.0.0:8000,
or

```
python3 -m http.server 8001
```

to specify alternate port (default: 8000).

The `-b` option can be used to specify an alternate bind address (default: 0.0.0.0 i.e all interfaces), e.g.

```
python3 -m http.server -b 127.0.0.1 8001
```

### With NPM

Only once:
```
npm install
```

then
```
npm start
```

## Npm with Docker

**Note**: the following commands have been integrated in the `./install.sh` and `./start.sh` scripts.

First, call `npm install`:

```sh
docker run --rm -it --name revealjs -v "$PWD":/usr/src/app -w /usr/src/app node npm install
```

Then, update `revealjs/gulpfile.js` to serve files from `./` rather than from `./revealjs/`:

```sh
sed -i "s:const root = yargs.argv.root || '.':const root = yargs.argv.root || '../':" gulpfile.js
```

Finally, call `npm start` and open the web browser at `http://127.0.0.1:8000`:

```sh
docker run --rm -it --name revealjs -v "$PWD":/usr/src/app -w /usr/src/app -p 8000:8000 -p 35729:35729 node npm start --prefix revealjs/ -- --host=0.0.0.0
```

## Deploy on slides.jdhp.org with Ansible

```sh
./ansible_playbook.yml -i hosts
```
